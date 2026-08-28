# Copyright (c) 2023 CEF Python, see the Authors file.
# All rights reserved. Licensed under BSD 3-clause license.
# Project website: https://github.com/cztomczak/cefpython

from libcpp cimport bool as cpp_bool
from cef_types cimport int64
from cef_types cimport uint32
from cef_string cimport CefString

cdef extern from "include/cef_download_item.h":

    cdef cppclass CefDownloadItem:
          cpp_bool IsValid()
          cpp_bool IsInProgress()
          cpp_bool IsComplete()
          cpp_bool IsCanceled()
          int64 GetCurrentSpeed()
          int GetPercentComplete()
          int64 GetTotalBytes()
          int64 GetReceivedBytes()
#          CefBaseTime GetStartTime()
#          CefBaseTime GetEndTime()
          CefString GetFullPath()
#          uint32 GetId()
          CefString GetURL()
          CefString GetOriginalUrl()
          CefString GetSuggestedFileName()
          CefString GetContentDisposition()
          CefString GetMimeType()
