// Copyright (c) 2021 Marshall A. Greenblatt. All rights reserved.
//
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions are
// met:
//
//    * Redistributions of source code must retain the above copyright
// notice, this list of conditions and the following disclaimer.
//    * Redistributions in binary form must reproduce the above
// copyright notice, this list of conditions and the following disclaimer
// in the documentation and/or other materials provided with the
// distribution.
//    * Neither the name of Google Inc. nor the name Chromium Embedded
// Framework nor the names of its contributors may be used to endorse
// or promote products derived from this software without specific prior
// written permission.
//
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
// "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
// LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
// A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
// OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
// SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
// LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
// DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
// THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
// (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
// OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
//
// ---------------------------------------------------------------------------
//
// This file was generated by the make_version_header.py tool.
//

#ifndef CEF_INCLUDE_CEF_VERSION_H_
#define CEF_INCLUDE_CEF_VERSION_H_

#define CEF_VERSION "86.0.24+g85e79d4+chromium-86.0.4240.198"
#define CEF_VERSION_MAJOR 86
#define CEF_VERSION_MINOR 0
#define CEF_VERSION_PATCH 24
#define CEF_COMMIT_NUMBER 2278
#define CEF_COMMIT_HASH "85e79d418db1999bb22fdead4c178e1b0694bb4c"
#define COPYRIGHT_YEAR 2021

#define CHROME_VERSION_MAJOR 86
#define CHROME_VERSION_MINOR 0
#define CHROME_VERSION_BUILD 4240
#define CHROME_VERSION_PATCH 198

#define DO_MAKE_STRING(p) #p
#define MAKE_STRING(p) DO_MAKE_STRING(p)

#ifndef APSTUDIO_HIDDEN_SYMBOLS

#include "include/internal/cef_export.h"

#ifdef __cplusplus
extern "C" {
#endif

// Returns CEF version information for the libcef library. The |entry|
// parameter describes which version component will be returned:
// 0 - CEF_VERSION_MAJOR
// 1 - CEF_VERSION_MINOR
// 2 - CEF_VERSION_PATCH
// 3 - CEF_COMMIT_NUMBER
// 4 - CHROME_VERSION_MAJOR
// 5 - CHROME_VERSION_MINOR
// 6 - CHROME_VERSION_BUILD
// 7 - CHROME_VERSION_PATCH
///
CEF_EXPORT int cef_version_info(int entry);

#ifdef __cplusplus
}
#endif

#endif  // APSTUDIO_HIDDEN_SYMBOLS

#endif  // CEF_INCLUDE_CEF_VERSION_H_
