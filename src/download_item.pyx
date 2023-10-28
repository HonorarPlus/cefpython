# Copyright (c) 2023 CEF Python, see the Authors file.
# All rights reserved. Licensed under BSD 3-clause license.
# Project website: https://github.com/cztomczak/cefpython

include "cefpython.pyx"

# noinspection PyUnresolvedReferences
cimport cef_types


cdef PyDownloadItem CreatePyDownloadItem(CefRefPtr[CefDownloadItem] cefDownloadItem):
    cdef PyDownloadItem pyDownloadItem = PyDownloadItem()
    pyDownloadItem.cefDownloadItem = cefDownloadItem
    return pyDownloadItem

cdef class PyDownloadItem:
    cdef CefRefPtr[CefDownloadItem] cefDownloadItem
          
    cpdef py_bool IsValid(self):
        return self.cefDownloadItem.get().IsValid()
    
    cpdef py_bool IsInProgress(self):
        return self.cefDownloadItem.get().IsInProgress()
    
    cpdef py_bool IsComplete(self):
        return self.cefDownloadItem.get().IsComplete()
    
    cpdef py_bool IsCanceled(self):
        return self.cefDownloadItem.get().IsCanceled()

    cpdef py_bool IsInterrupted(self):
        return self.cefDownloadItem.get().IsInterrupted()
    
    cpdef int64_t GetCurrentSpeed(self) except *:
        return self.cefDownloadItem.get().GetCurrentSpeed()
    
    cpdef int GetPercentComplete(self) except *:
        return self.cefDownloadItem.get().GetPercentComplete()
    
    cpdef int64_t GetTotalBytes(self) except *:
        return self.cefDownloadItem.get().GetTotalBytes()
    
    cpdef int64_t GetReceivedBytes(self) except *:
        return self.cefDownloadItem.get().GetReceivedBytes()
#          CefBaseTime GetStartTime()
#          CefBaseTime GetEndTime()
    cpdef py_string GetFullPath(self):
        return CefToPyString(self.cefDownloadItem.get().GetFullPath())
#          uint32 GetId()
    cpdef py_string GetURL(self):
        return CefToPyString(self.cefDownloadItem.get().GetURL())
    
    cpdef py_string GetOriginalUrl(self):
        return CefToPyString(self.cefDownloadItem.get().GetOriginalUrl())
    
    cpdef py_string GetSuggestedFileName(self):
        return CefToPyString(self.cefDownloadItem.get().GetSuggestedFileName())
    
    cpdef py_string GetContentDisposition(self):
        return CefToPyString(self.cefDownloadItem.get().GetContentDisposition())
    
    cpdef py_string GetMimeType(self):
        return CefToPyString(self.cefDownloadItem.get().GetMimeType())
