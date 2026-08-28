# Copyright (c) 2026 CEF Python, see the Authors file.
# All rights reserved. Licensed under BSD 3-clause license.
# Project website: https://github.com/cztomczak/cefpython

include "../cefpython.pyx"
include "../browser.pyx"

cimport cef_types

PERMISSION_TYPE_NONE = cef_types.CEF_PERMISSION_TYPE_NONE
PERMISSION_TYPE_CLIPBOARD = cef_types.CEF_PERMISSION_TYPE_CLIPBOARD
PERMISSION_RESULT_ACCEPT = cef_types.CEF_PERMISSION_RESULT_ACCEPT
PERMISSION_RESULT_DENY = cef_types.CEF_PERMISSION_RESULT_DENY
PERMISSION_RESULT_DISMISS = cef_types.CEF_PERMISSION_RESULT_DISMISS
PERMISSION_RESULT_IGNORE = cef_types.CEF_PERMISSION_RESULT_IGNORE


cdef PyPermissionPromptCallback CreatePyPermissionPromptCallback(
        CefRefPtr[CefPermissionPromptCallback] cef_callback):
    cdef PyPermissionPromptCallback py_callback = PyPermissionPromptCallback()
    py_callback.cef_callback = cef_callback
    return py_callback


cdef class PyPermissionPromptCallback:
    cdef CefRefPtr[CefPermissionPromptCallback] cef_callback

    cpdef py_void Continue(self, int result):
        self.cef_callback.get().Continue(
                <cef_types.cef_permission_request_result_t>result)


cdef public cpp_bool PermissionHandler_OnShowPermissionPrompt(
        CefRefPtr[CefBrowser] cef_browser,
        uint64_t prompt_id,
        const CefString& requesting_origin,
        uint32_t requested_permissions,
        CefRefPtr[CefPermissionPromptCallback] callback
        ) except * with gil:
    cdef PyBrowser py_browser
    cdef PyPermissionPromptCallback py_callback
    cdef object client_callback
    cdef py_bool return_value
    try:
        py_browser = GetPyBrowser(cef_browser, "OnShowPermissionPrompt")
        py_callback = CreatePyPermissionPromptCallback(callback)
        client_callback = py_browser.GetClientCallback(
                "OnShowPermissionPrompt")
        if client_callback:
            return_value = client_callback(
                    browser=py_browser,
                    prompt_id=prompt_id,
                    requesting_origin=CefToPyString(requesting_origin),
                    requested_permissions=requested_permissions,
                    callback=py_callback)
            return bool(return_value)
        return False
    except:
        (exc_type, exc_value, exc_trace) = sys.exc_info()
        sys.excepthook(exc_type, exc_value, exc_trace)
        return False
