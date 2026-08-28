# Copyright (c) 2012 CEF Python, see the Authors file.
# All rights reserved. Licensed under BSD 3-clause license.
# Project website: https://github.com/cztomczak/cefpython

from libcpp cimport bool as cpp_bool

cdef extern from "client_handler/client_handler.h":

    cdef cppclass ClientHandler:
        ClientHandler(cpp_bool owns_top_level_window)
