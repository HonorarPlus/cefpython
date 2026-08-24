// Copyright (c) 2026 CEF Python, see the Authors file.
// All rights reserved. Licensed under BSD 3-clause license.
// Project website: https://github.com/cztomczak/cefpython

#pragma once

#include "common/cefpython_public_api.h"
#include "include/cef_permission_handler.h"


class PermissionHandler : public CefPermissionHandler
{
public:
    PermissionHandler() = default;
    virtual ~PermissionHandler() = default;

    bool OnShowPermissionPrompt(
            CefRefPtr<CefBrowser> browser,
            uint64_t prompt_id,
            const CefString& requesting_origin,
            uint32_t requested_permissions,
            CefRefPtr<CefPermissionPromptCallback> callback) override;

private:
    IMPLEMENT_REFCOUNTING(PermissionHandler);
};
