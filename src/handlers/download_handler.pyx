# Copyright (c) 2023 CEF Python, see the Authors file.
# All rights reserved. Licensed under BSD 3-clause license.
# Project website: https://github.com/cztomczak/cefpython

include "../cefpython.pyx"
include "../browser.pyx"

cimport cef_types
cimport cef_download_item

from cef_types cimport TID_UI

cdef PyBeforeDownloadCallback CreatePyBeforeDownloadCallback(CefRefPtr[CefBeforeDownloadCallback] callback):
    cdef PyBeforeDownloadCallback pyBeforeDownloadCallback = PyBeforeDownloadCallback()
    pyBeforeDownloadCallback.cefBeforeDownloadCallback = callback
    return pyBeforeDownloadCallback

cdef PyDownloadItemCallback CreatePyDownloadUpdatedCallback(CefRefPtr[CefDownloadItemCallback] callback):
    cdef PyDownloadItemCallback pyDownloadItemCallback = PyDownloadItemCallback()
    pyDownloadItemCallback.cefDownloadItemCallback = callback
    return pyDownloadItemCallback

cdef class PyBeforeDownloadCallback:
    cdef CefRefPtr[CefBeforeDownloadCallback] cefBeforeDownloadCallback
    
    cpdef void Continue(self, py_string download_path, py_bool show_dialog) except *:
        cdef CefString cefString
        PyToCefString(download_path, cefString)
        self.cefBeforeDownloadCallback.get().Continue(cefString, bool(show_dialog))

cdef class PyDownloadItemCallback:
    cdef CefRefPtr[CefDownloadItemCallback] cefDownloadItemCallback
    
    cpdef void Cancel(self) except *:
        self.cefDownloadItemCallback.get().Cancel()
    
    cpdef void Pause(self) except *:
        self.cefDownloadItemCallback.get().Pause()
    
    cpdef void Resume(self) except *:
        self.cefDownloadItemCallback.get().Resume()

cdef public cpp_bool DownloadHandler_CanDownload(
    CefRefPtr[CefBrowser] cefBrowser,
    const CefString& url,
    const CefString& requestMethod) except * with gil:
    cdef PyBrowser browser
    cdef py_bool retval
    cdef py_string pyUrl
    try:
        assert IsThread(TID_UI), "Must be called on the UI thread"
        browser = GetPyBrowser(cefBrowser, "CanDownload")
        callback = browser.GetClientCallback("CanDownload")
        pyUrl = CefToPyString(url)
        pyRequestMethod = CefToPyString(requestMethod)
        if callback:
            retval = callback(browser=browser, url=pyUrl, request_method=pyRequestMethod)
            return bool(retval)
        else:
            return False
    except:
        (exc_type, exc_value, exc_trace) = sys.exc_info()
        sys.excepthook(exc_type, exc_value, exc_trace)
    
cdef public void DownloadHandler_OnBeforeDownload(
    CefRefPtr[CefBrowser] cefBrowser,
    CefRefPtr[CefDownloadItem] downloadItem,
    const CefString& suggestedName,
    CefRefPtr[CefBeforeDownloadCallback] callback
    ) except * with gil:
    cdef PyBrowser browser
    cdef py_string pySuggestedName
    cdef PyDownloadItem pyDownloadItem
    cdef PyBeforeDownloadCallback pyBeforeDownloadCallback
    try:
        assert IsThread(TID_UI), "Must be called on the UI thread"
        browser = GetPyBrowser(cefBrowser, "OnBeforeDownload")
        callback_ = browser.GetClientCallback("OnBeforeDownload")
        pySuggestedName = CefToPyString(suggestedName)
        pyDownloadItem = CreatePyDownloadItem(downloadItem)
        pyBeforeDownloadCallback = CreatePyBeforeDownloadCallback(callback)
        if callback_:
            callback_(browser=browser, download_item=pyDownloadItem, suggested_name=pySuggestedName, callback=pyBeforeDownloadCallback)
    except:
        (exc_type, exc_value, exc_trace) = sys.exc_info()
        sys.excepthook(exc_type, exc_value, exc_trace)

cdef public void DownloadHandler_OnDownloadUpdated(
    CefRefPtr[CefBrowser] cefBrowser,
    CefRefPtr[CefDownloadItem] downloadItem,
    CefRefPtr[CefDownloadItemCallback] callback
    ) except * with gil:
    cdef PyBrowser browser
    cdef PyDownloadItem pyDownloadItem
    try:
        assert IsThread(TID_UI), "Must be called on the UI thread"
        browser = GetPyBrowser(cefBrowser, "OnDownloadUpdated")
        callback_ = browser.GetClientCallback("OnDownloadUpdated")
        pyDownloadItem = CreatePyDownloadItem(downloadItem)
        pyDownloadUpdatedCallback = CreatePyDownloadUpdatedCallback(callback)
        if callback_:
            callback_(browser=browser, download_item=pyDownloadItem, callback=pyDownloadUpdatedCallback)
    except:
        (exc_type, exc_value, exc_trace) = sys.exc_info()
        sys.excepthook(exc_type, exc_value, exc_trace)
