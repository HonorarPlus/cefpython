# Copyright (c) 2012 CEF Python, see the Authors file.
# All rights reserved. Licensed under BSD 3-clause license.
# Project website: https://github.com/cztomczak/cefpython

include "compile_time_constants.pxi"

from libcpp cimport bool as cpp_bool
from cef_types cimport CefRect, cef_runtime_style_t

cdef extern from "include/internal/cef_linux.h":

    ctypedef unsigned long CefWindowHandle
    ctypedef unsigned long CefCursorHandle

    cdef cppclass CefWindowInfo:
        cef_runtime_style_t runtime_style
        void SetAsChild(CefWindowHandle parent,
                        const CefRect& windowRect)
        void SetAsWindowless(CefWindowHandle parent)

    cdef cppclass CefMainArgs:
        CefMainArgs()
        CefMainArgs(int argc_arg, char** argv_arg)
