# Copyright (c) 2026 CEF Python, see the Authors file.
# All rights reserved. Licensed under BSD 3-clause license.
# Project website: https://github.com/cztomczak/cefpython

from cef_types cimport cef_permission_request_result_t

cdef extern from "include/cef_permission_handler.h":
    cdef cppclass CefPermissionPromptCallback:
        void Continue(cef_permission_request_result_t result)
