// Copyright (c) 2026 CEF Python, see the Authors file.
// All rights reserved. Licensed under BSD 3-clause license.
// Project website: https://github.com/cztomczak/cefpython

#include "permission_handler.h"


bool PermissionHandler::OnShowPermissionPrompt(
        CefRefPtr<CefBrowser> browser,
        uint64_t prompt_id,
        const CefString& requesting_origin,
        uint32_t requested_permissions,
        CefRefPtr<CefPermissionPromptCallback> callback)
{
    REQUIRE_UI_THREAD();
    return PermissionHandler_OnShowPermissionPrompt(
            browser,
            prompt_id,
            requesting_origin,
            requested_permissions,
            callback);
}
