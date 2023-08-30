# Copyright (c) 2023 CEF Python, see the Authors file.
# All rights reserved. Licensed under BSD 3-clause license.
# Project website: https://github.com/cztomczak/cefpython

from cef_string cimport CefString
from libcpp cimport bool as cpp_bool

cdef extern from "include/cef_download_handler.h":

    cdef cppclass CefBeforeDownloadCallback:
        void Continue(const CefString& download_path, cpp_bool show_dialog)
        
    
    cdef cppclass CefDownloadItemCallback:
        void Cancel()
        void Pause()
        void Resume()
