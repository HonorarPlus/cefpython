#include "print_callback.h"

void PdfPrintCallback::OnPdfPrintFinished(const CefString& path, bool ok
        ) {
    REQUIRE_UI_THREAD();
    std::string msg = "[Browser process] PDF Printing Completed, saved to: ";
    msg.append(path);
    LOG(INFO) << msg.c_str();
    PrintToPDF_OnPdfPrintFinished(browser_, path, ok);
}
