# Copyright (c) 2023 CEF Python, see the Authors file.
# All rights reserved. Licensed under BSD 3-clause license.
# Project website: https://github.com/cztomczak/cefpython

from libcpp cimport bool as cpp_bool
from cef_types cimport int64_t
from cef_types cimport uint32_t
from cef_string cimport CefString

cdef extern from "include/cef_download_item.h":

    cdef cppclass CefDownloadItem:
          cpp_bool IsValid()
          cpp_bool IsInProgress()
          cpp_bool IsComplete()
          cpp_bool IsCanceled()
          cpp_bool IsInterrupted()
#          DownloadInterruptReason GetInterruptReason()
          int64_t GetCurrentSpeed()
          int GetPercentComplete()
          int64_t GetTotalBytes()
          int64_t GetReceivedBytes()
#          CefBaseTime GetStartTime()
#          CefBaseTime GetEndTime()
          CefString GetFullPath()
#          uint32_t GetId()
          CefString GetURL()
          CefString GetOriginalUrl()
          CefString GetSuggestedFileName()
          CefString GetContentDisposition()
          CefString GetMimeType()
