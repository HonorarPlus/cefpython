// Copyright (c) 2013 CEF Python, see the Authors file.
// All rights reserved. Licensed under BSD 3-clause license.
// Project website: https://github.com/cztomczak/cefpython

#include "cefpython_app.h"

#if defined(OS_MAC)
#include <mach-o/dyld.h>

#include <filesystem>
#include <memory>

#include "include/cef_sandbox_mac.h"
#include "include/wrapper/cef_library_loader.h"

namespace {

bool LoadCefFramework() {
	uint32_t path_size = 0;
	_NSGetExecutablePath(nullptr, &path_size);
	std::unique_ptr<char[]> executable_path(new char[path_size]);
	if (_NSGetExecutablePath(executable_path.get(), &path_size) != 0) {
		return false;
	}

	auto package_path = std::filesystem::path(executable_path.get()).parent_path();
	if (package_path.filename() == "MacOS") {
		package_path = package_path.parent_path().parent_path().parent_path();
	}
	const auto framework_path = package_path
		/ "Chromium Embedded Framework.framework"
		/ "Chromium Embedded Framework";
	return cef_load_library(framework_path.c_str()) != 0;
}

}  // namespace
#endif

#if defined(OS_WIN)

#include <windows.h>
int APIENTRY wWinMain(HINSTANCE hInstance,
                      HINSTANCE hPrevInstance,
                      LPTSTR    lpCmdLine,
                      int       nCmdShow)
{
	UNREFERENCED_PARAMETER(hPrevInstance);
	UNREFERENCED_PARAMETER(lpCmdLine);

	// lpCmdLine does not include program name argument, must
	// use GetCommandLineW(). Cannot use CefCommandLine::GetGlobalCommandLine,
	// as CEF was not yet initialized.
	CefRefPtr<CefCommandLine> command_line = \
	        CefCommandLine::CreateCommandLine();
    command_line->InitFromString(GetCommandLineW());
    if (command_line->HasSwitch("enable-high-dpi-support")) {
	    SetProcessDpiAwarenessContext(DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2);
	}

	CefMainArgs mainArgs(hInstance);

#else // defined(OS_WIN)

int main(int argc, char **argv)
{
	#if defined(OS_MAC)
	CefScopedSandboxContext sandbox_context;
	if (!sandbox_context.Initialize(argc, argv)) {
		return 1;
	}

		if (!LoadCefFramework()) {
			return 1;
		}
	#endif

	CefMainArgs mainArgs(argc, argv);

#endif // Mac, Linux

	CefRefPtr<CefPythonApp> app(new CefPythonApp);
	int exitCode = CefExecuteProcess(mainArgs, app.get(), NULL);
	return exitCode;
}
