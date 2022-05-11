from cef_string cimport CefString
from libcpp cimport bool as cpp_bool
from cef_ptr cimport CefRefPtr
from cef_browser cimport CefBrowser


cdef extern from "client_handler/print_callback.h":

    cdef cppclass PdfPrintCallback:
        PdfPrintCallback(CefRefPtr[CefBrowser] browser)
