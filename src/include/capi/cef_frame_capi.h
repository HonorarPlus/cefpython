// Copyright (c) 2024 Marshall A. Greenblatt. All rights reserved.
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
// This file was generated by the CEF translator tool and should not edited
// by hand. See the translator.README.txt file in the tools directory for
// more information.
//
// $hash=7294486141b2377198e994048a768db4a7cb9cd0$
//

#ifndef CEF_INCLUDE_CAPI_CEF_FRAME_CAPI_H_
#define CEF_INCLUDE_CAPI_CEF_FRAME_CAPI_H_
#pragma once

#include "include/capi/cef_base_capi.h"
#include "include/capi/cef_dom_capi.h"
#include "include/capi/cef_process_message_capi.h"
#include "include/capi/cef_request_capi.h"
#include "include/capi/cef_stream_capi.h"
#include "include/capi/cef_string_visitor_capi.h"

#ifdef __cplusplus
extern "C" {
#endif

struct _cef_browser_t;
struct _cef_urlrequest_client_t;
struct _cef_urlrequest_t;
struct _cef_v8context_t;

///
/// Structure used to represent a frame in the browser window. When used in the
/// browser process the functions of this structure may be called on any thread
/// unless otherwise indicated in the comments. When used in the render process
/// the functions of this structure may only be called on the main thread.
///
typedef struct _cef_frame_t {
  ///
  /// Base structure.
  ///
  cef_base_ref_counted_t base;

  ///
  /// True if this object is currently attached to a valid frame.
  ///
  int(CEF_CALLBACK* is_valid)(struct _cef_frame_t* self);

  ///
  /// Execute undo in this frame.
  ///
  void(CEF_CALLBACK* undo)(struct _cef_frame_t* self);

  ///
  /// Execute redo in this frame.
  ///
  void(CEF_CALLBACK* redo)(struct _cef_frame_t* self);

  ///
  /// Execute cut in this frame.
  ///
  void(CEF_CALLBACK* cut)(struct _cef_frame_t* self);

  ///
  /// Execute copy in this frame.
  ///
  void(CEF_CALLBACK* copy)(struct _cef_frame_t* self);

  ///
  /// Execute paste in this frame.
  ///
  void(CEF_CALLBACK* paste)(struct _cef_frame_t* self);

  ///
  /// Execute delete in this frame.
  ///
  void(CEF_CALLBACK* del)(struct _cef_frame_t* self);

  ///
  /// Execute select all in this frame.
  ///
  void(CEF_CALLBACK* select_all)(struct _cef_frame_t* self);

  ///
  /// Save this frame's HTML source to a temporary file and open it in the
  /// default text viewing application. This function can only be called from
  /// the browser process.
  ///
  void(CEF_CALLBACK* view_source)(struct _cef_frame_t* self);

  ///
  /// Retrieve this frame's HTML source as a string sent to the specified
  /// visitor.
  ///
  void(CEF_CALLBACK* get_source)(struct _cef_frame_t* self,
                                 struct _cef_string_visitor_t* visitor);

  ///
  /// Retrieve this frame's display text as a string sent to the specified
  /// visitor.
  ///
  void(CEF_CALLBACK* get_text)(struct _cef_frame_t* self,
                               struct _cef_string_visitor_t* visitor);

  ///
  /// Load the request represented by the |request| object.
  ///
  /// WARNING: This function will fail with "bad IPC message" reason
  /// INVALID_INITIATOR_ORIGIN (213) unless you first navigate to the request
  /// origin using some other mechanism (LoadURL, link click, etc).
  ///
  void(CEF_CALLBACK* load_request)(struct _cef_frame_t* self,
                                   struct _cef_request_t* request);

  ///
  /// Load the specified |url|.
  ///
  void(CEF_CALLBACK* load_url)(struct _cef_frame_t* self,
                               const cef_string_t* url);

  ///
  /// Execute a string of JavaScript code in this frame. The |script_url|
  /// parameter is the URL where the script in question can be found, if any.
  /// The renderer may request this URL to show the developer the source of the
  /// error.  The |start_line| parameter is the base line number to use for
  /// error reporting.
  ///
  void(CEF_CALLBACK* execute_java_script)(struct _cef_frame_t* self,
                                          const cef_string_t* code,
                                          const cef_string_t* script_url,
                                          int start_line);

  ///
  /// Returns true (1) if this is the main (top-level) frame.
  ///
  int(CEF_CALLBACK* is_main)(struct _cef_frame_t* self);

  ///
  /// Returns true (1) if this is the focused frame.
  ///
  int(CEF_CALLBACK* is_focused)(struct _cef_frame_t* self);

  ///
  /// Returns the name for this frame. If the frame has an assigned name (for
  /// example, set via the iframe "name" attribute) then that value will be
  /// returned. Otherwise a unique name will be constructed based on the frame
  /// parent hierarchy. The main (top-level) frame will always have an NULL name
  /// value.
  ///
  // The resulting string must be freed by calling cef_string_userfree_free().
  cef_string_userfree_t(CEF_CALLBACK* get_name)(struct _cef_frame_t* self);

  ///
  /// Returns the globally unique identifier for this frame or < 0 if the
  /// underlying frame does not yet exist.
  ///
  int64_t(CEF_CALLBACK* get_identifier)(struct _cef_frame_t* self);

  ///
  /// Returns the parent of this frame or NULL if this is the main (top-level)
  /// frame.
  ///
  struct _cef_frame_t*(CEF_CALLBACK* get_parent)(struct _cef_frame_t* self);

  ///
  /// Returns the URL currently loaded in this frame.
  ///
  // The resulting string must be freed by calling cef_string_userfree_free().
  cef_string_userfree_t(CEF_CALLBACK* get_url)(struct _cef_frame_t* self);

  ///
  /// Returns the browser that this frame belongs to.
  ///
  struct _cef_browser_t*(CEF_CALLBACK* get_browser)(struct _cef_frame_t* self);

  ///
  /// Get the V8 context associated with the frame. This function can only be
  /// called from the render process.
  ///
  struct _cef_v8context_t*(CEF_CALLBACK* get_v8context)(
      struct _cef_frame_t* self);

  ///
  /// Visit the DOM document. This function can only be called from the render
  /// process.
  ///
  void(CEF_CALLBACK* visit_dom)(struct _cef_frame_t* self,
                                struct _cef_domvisitor_t* visitor);

  ///
  /// Create a new URL request that will be treated as originating from this
  /// frame and the associated browser. Use cef_urlrequest_t::Create instead if
  /// you do not want the request to have this association, in which case it may
  /// be handled differently (see documentation on that function). A request
  /// created with this function may only originate from the browser process,
  /// and will behave as follows:
  ///   - It may be intercepted by the client via CefResourceRequestHandler or
  ///     CefSchemeHandlerFactory.
  ///   - POST data may only contain a single element of type PDE_TYPE_FILE or
  ///     PDE_TYPE_BYTES.
  ///
  /// The |request| object will be marked as read-only after calling this
  /// function.
  ///
  struct _cef_urlrequest_t*(CEF_CALLBACK* create_urlrequest)(
      struct _cef_frame_t* self,
      struct _cef_request_t* request,
      struct _cef_urlrequest_client_t* client);

  ///
  /// Send a message to the specified |target_process|. Ownership of the message
  /// contents will be transferred and the |message| reference will be
  /// invalidated. Message delivery is not guaranteed in all cases (for example,
  /// if the browser is closing, navigating, or if the target process crashes).
  /// Send an ACK message back from the target process if confirmation is
  /// required.
  ///
  void(CEF_CALLBACK* send_process_message)(
      struct _cef_frame_t* self,
      cef_process_id_t target_process,
      struct _cef_process_message_t* message);
} cef_frame_t;

#ifdef __cplusplus
}
#endif

#endif  // CEF_INCLUDE_CAPI_CEF_FRAME_CAPI_H_
