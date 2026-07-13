# Copyright (c) 2012 CEF Python, see the Authors file.
# All rights reserved. Licensed under BSD 3-clause license.
# Project website: https://github.com/cztomczak/cefpython

include "compile_time_constants.pxi"

# noinspection PyUnresolvedReferences
from windows cimport HWND, RECT, HINSTANCE, HCURSOR
from cef_string cimport CefString
from libcpp cimport bool as cpp_bool
from libc.stdint cimport uint32_t
from cef_types cimport CefRect, cef_runtime_style_t

cdef extern from "include/internal/cef_win.h":

    # noinspection PyUnresolvedReferences
    ctypedef HWND CefWindowHandle
    # noinspection PyUnresolvedReferences
    ctypedef HCURSOR CefCursorHandle

    cdef cppclass CefWindowInfo:
        uint32_t style
        cef_runtime_style_t runtime_style
        void SetAsChild(CefWindowHandle parent,
                        const CefRect& windowRect)
        void SetAsPopup(CefWindowHandle parent,
                        const CefString& windowName)
        void SetAsWindowless(CefWindowHandle parent)

    cdef cppclass CefMainArgs:
        CefMainArgs()
        CefMainArgs(HINSTANCE hInstance)
        
    cdef void CefSetOSModalLoop(cpp_bool osModalLoop) nogil
