# Copyright (c) 2012 CEF Python, see the Authors file.
# All rights reserved. Licensed under BSD 3-clause license.
# Project website: https://github.com/cztomczak/cefpython

include "compile_time_constants.pxi"

from libcpp cimport bool as cpp_bool
# noinspection PyUnresolvedReferences
from libc.stddef cimport wchar_t
# noinspection PyUnresolvedReferences
from libc.stdint cimport int16_t, uint16_t, int32_t, uint32_t, int64_t, uint64_t
from cef_string cimport cef_string_t
# noinspection PyUnresolvedReferences
from libc.limits cimport UINT_MAX

cdef extern from "include/internal/cef_types.h":

    # noinspection PyUnresolvedReferences
    ctypedef int32_t int32
    # noinspection PyUnresolvedReferences
    ctypedef uint32_t uint32
    # noinspection PyUnresolvedReferences
    ctypedef int64_t int64
    # noinspection PyUnresolvedReferences
    ctypedef uint64_t uint64

    IF UNAME_SYSNAME == "Windows":
        # noinspection PyUnresolvedReferences
        #TODO: revisit me
        ctypedef uint16_t char16
    ELSE:
        ctypedef unsigned short char16

    ctypedef uint32_t cef_color_t

    ctypedef struct CefSettings:
        # size_t size
        int no_sandbox
        cef_string_t browser_subprocess_path
        cef_string_t framework_dir_path
        cef_string_t main_bundle_path
        int chrome_runtime
        int multi_threaded_message_loop
        int external_message_pump
        int windowless_rendering_enabled
        int command_line_args_disabled
        cef_string_t cache_path
        cef_string_t root_cache_path
        int persist_session_cookies
        int persist_user_preferences
        cef_string_t user_agent
        cef_string_t user_agent_product
        cef_string_t locale
        cef_string_t log_file
        int log_severity
        int log_items # not exposed.
        cef_string_t javascript_flags
        cef_string_t resources_dir_path
        cef_string_t locales_dir_path
        int pack_loading_disabled
        int remote_debugging_port
        int uncaught_exception_stack_size
        cef_color_t background_color
        cef_string_t accept_language_list
        cef_string_t cookieable_schemes_list
        int cookieable_schemes_exclude_defaults
        cef_string_t chrome_policy_id

    ctypedef enum cef_pdf_print_margin_type_t:
        PDF_PRINT_MARGIN_DEFAULT,
        PDF_PRINT_MARGIN_NONE,
        PDF_PRINT_MARGIN_MINIMUM,
        PDF_PRINT_MARGIN_CUSTOM,

    ctypedef struct CefPdfPrintSettings:
        int landscape
        int print_background
        double scale
        double paper_width
        double paper_height
        int prefer_css_page_size
        cef_pdf_print_margin_type_t margin_type
        double margin_top
        double margin_right
        double margin_bottom
        double margin_left
        cef_string_t page_ranges
        int display_header_footer
        cef_string_t header_template
        cef_string_t footer_template
        int generate_tagged_pdf
        int generate_document_outline

    ctypedef struct CefBrowserSettings:
        int windowless_frame_rate
        cef_string_t standard_font_family
        cef_string_t fixed_font_family
        cef_string_t serif_font_family
        cef_string_t sans_serif_font_family
        cef_string_t cursive_font_family
        cef_string_t fantasy_font_family
        int default_font_size
        int default_fixed_font_size
        int minimum_font_size
        int minimum_logical_font_size
        cef_string_t default_encoding
        cef_state_t remote_fonts
        cef_state_t javascript
        cef_state_t javascript_close_windows
        cef_state_t javascript_access_clipboard
        cef_state_t javascript_dom_paste
        cef_state_t image_loading
        cef_state_t image_shrink_standalone_to_fit
        cef_state_t text_area_resize
        cef_state_t tab_to_links
        cef_state_t local_storage
        cef_state_t databases
        cef_state_t webgl
        cef_color_t background_color
        # chrome_status_bubble
        # chrome_zoom_bubble

    cdef cppclass CefRect:
        int x, y, width, height
        CefRect()
        CefRect(int x, int y, int width, int height)

    cdef cppclass CefSize:
        int width, height
        CefSize()
        CefSize(int width, int height)

    cdef cppclass CefPoint:
        int x
        int y

    ctypedef struct CefRequestContextSettings:
        pass

    ctypedef enum cef_log_severity_t:
        LOGSEVERITY_DEFAULT,
        LOGSEVERITY_VERBOSE,
        LOGSEVERITY_DEBUG = LOGSEVERITY_VERBOSE,
        LOGSEVERITY_INFO,
        LOGSEVERITY_WARNING,
        LOGSEVERITY_ERROR,
        LOGSEVERITY_FATAL,
        LOGSEVERITY_DISABLE = 99,
        
    ctypedef enum cef_log_items_t:
        LOG_ITEMS_DEFAULT = 0,
        LOG_ITEMS_NONE = 1,
        LOG_ITEMS_FLAG_PROCESS_ID = 1 << 1,
        LOG_ITEMS_FLAG_THREAD_ID = 1 << 2,
        LOG_ITEMS_FLAG_TIME_STAMP = 1 << 3,
        LOG_ITEMS_FLAG_TICK_COUNT = 1 << 4,

    ctypedef enum cef_thread_id_t:
        TID_UI,
        TID_FILE_BACKGROUND
        TID_FILE_USER_VISIBLE,
        TID_FILE_USER_BLOCKING,
        TID_PROCESS_LAUNCHER,
        TID_IO,
        TID_RENDERER

    ctypedef enum cef_v8_propertyattribute_t:
        V8_PROPERTY_ATTRIBUTE_NONE = 0,       # Writeable, Enumerable,
        #  Configurable
        V8_PROPERTY_ATTRIBUTE_READONLY = 1 << 0,  # Not writeable
        V8_PROPERTY_ATTRIBUTE_DONTENUM = 1 << 1,  # Not enumerable
        V8_PROPERTY_ATTRIBUTE_DONTDELETE = 1 << 2   # Not configurable

    ctypedef enum cef_navigation_type_t:
        NAVIGATION_LINK_CLICKED = 0,
        NAVIGATION_FORM_SUBMITTED,
        NAVIGATION_BACK_FORWARD,
        NAVIGATION_RELOAD,
        NAVIGATION_FORM_RESUBMITTED,
        NAVIGATION_OTHER,

    ctypedef enum cef_process_id_t:
        PID_BROWSER,
        PID_RENDERER,

    ctypedef enum cef_state_t:
        STATE_DEFAULT = 0,
        STATE_ENABLED,
        STATE_DISABLED,

    ctypedef enum cef_postdataelement_type_t:
        PDE_TYPE_EMPTY  = 0,
        PDE_TYPE_BYTES,
        PDE_TYPE_FILE,

    # WebRequest
    ctypedef enum cef_urlrequest_flags_t:
        UR_FLAG_NONE = 0,
        UR_FLAG_SKIP_CACHE = 1 << 0,
        UR_FLAG_ONLY_FROM_CACHE = 1 << 1,
        UR_FLAG_DISABLE_CACHE = 1 << 2,
        UR_FLAG_ALLOW_STORED_CREDENTIALS = 1 << 3,
        UR_FLAG_REPORT_UPLOAD_PROGRESS = 1 << 4,
        UR_FLAG_NO_DOWNLOAD_DATA = 1 << 5,
        UR_FLAG_NO_RETRY_ON_5XX = 1 << 6,
        UR_FLAG_STOP_ON_REDIRECT = 1 << 7,

    # CefListValue, CefDictionaryValue - types.
    ctypedef enum cef_value_type_t:
        VTYPE_INVALID = 0,
        VTYPE_NULL,
        VTYPE_BOOL,
        VTYPE_INT,
        VTYPE_DOUBLE,
        VTYPE_STRING,
        VTYPE_BINARY,
        VTYPE_DICTIONARY,
        VTYPE_LIST,

    # KeyboardHandler
    ctypedef void* CefEventHandle
    ctypedef enum cef_key_event_type_t:
        KEYEVENT_RAWKEYDOWN = 0,
        KEYEVENT_KEYDOWN,
        KEYEVENT_KEYUP,
        KEYEVENT_CHAR
    ctypedef struct _cef_key_event_t:
        cef_key_event_type_t type
        uint32_t modifiers
        int windows_key_code
        int native_key_code
        int is_system_key
        uint16_t character
        uint16_t unmodified_character
        cpp_bool focus_on_editable_field
    ctypedef _cef_key_event_t CefKeyEvent
    ctypedef enum cef_event_flags_t:
        EVENTFLAG_NONE                = 0,
        EVENTFLAG_CAPS_LOCK_ON        = 1 << 0,
        EVENTFLAG_SHIFT_DOWN          = 1 << 1,
        EVENTFLAG_CONTROL_DOWN        = 1 << 2,
        EVENTFLAG_ALT_DOWN            = 1 << 3,
        EVENTFLAG_LEFT_MOUSE_BUTTON   = 1 << 4,
        EVENTFLAG_MIDDLE_MOUSE_BUTTON = 1 << 5,
        EVENTFLAG_RIGHT_MOUSE_BUTTON  = 1 << 6,
        # Mac OS-X command key.
        EVENTFLAG_COMMAND_DOWN        = 1 << 7,
        EVENTFLAG_NUM_LOCK_ON         = 1 << 8,
        EVENTFLAG_IS_KEY_PAD          = 1 << 9,
        EVENTFLAG_IS_LEFT             = 1 << 10,
        EVENTFLAG_IS_RIGHT            = 1 << 11,
        EVENTFLAG_ALTGR_DOWN          = 1 << 12,
        EVENTFLAG_IS_REPEAT           = 1 << 13,

    # Cookie priority values.
    ctypedef enum cef_cookie_priority_t:
        CEF_COOKIE_PRIORITY_LOW = -1,
        CEF_COOKIE_PRIORITY_MEDIUM = 0,
        CEF_COOKIE_PRIORITY_HIGH = 1,

    # Cookie same site values.
    ctypedef enum cef_cookie_same_site_t:
        CEF_COOKIE_SAME_SITE_UNSPECIFIED,
        CEF_COOKIE_SAME_SITE_NO_RESTRICTION,
        CEF_COOKIE_SAME_SITE_LAX_MODE,
        CEF_COOKIE_SAME_SITE_STRICT_MODE,

    # LoadHandler
    ctypedef enum cef_termination_status_t:
        TS_ABNORMAL_TERMINATION,
        TS_PROCESS_WAS_KILLED,
        TS_PROCESS_CRASHED,
        TS_PROCESS_OOM,

    ctypedef enum cef_errorcode_t:
        ERR_NONE = 0,
        ERR_FAILED = -2,
        ERR_ABORTED = -3,
        ERR_INVALID_ARGUMENT = -4,
        ERR_INVALID_HANDLE = -5,
        ERR_FILE_NOT_FOUND = -6,
        ERR_TIMED_OUT = -7,
        ERR_FILE_TOO_BIG = -8,
        ERR_UNEXPECTED = -9,
        ERR_ACCESS_DENIED = -10,
        ERR_NOT_IMPLEMENTED = -11,
        ERR_CONNECTION_CLOSED = -100,
        ERR_CONNECTION_RESET = -101,
        ERR_CONNECTION_REFUSED = -102,
        ERR_CONNECTION_ABORTED = -103,
        ERR_CONNECTION_FAILED = -104,
        ERR_NAME_NOT_RESOLVED = -105,
        ERR_INTERNET_DISCONNECTED = -106,
        ERR_SSL_PROTOCOL_ERROR = -107,
        ERR_ADDRESS_INVALID = -108,
        ERR_ADDRESS_UNREACHABLE = -109,
        ERR_SSL_CLIENT_AUTH_CERT_NEEDED = -110,
        ERR_TUNNEL_CONNECTION_FAILED = -111,
        ERR_NO_SSL_VERSIONS_ENABLED = -112,
        ERR_SSL_VERSION_OR_CIPHER_MISMATCH = -113,
        ERR_SSL_RENEGOTIATION_REQUESTED = -114,
        ERR_CERT_COMMON_NAME_INVALID = -200,
        ERR_CERT_DATE_INVALID = -201,
        ERR_CERT_AUTHORITY_INVALID = -202,
        ERR_CERT_CONTAINS_ERRORS = -203,
        ERR_CERT_NO_REVOCATION_MECHANISM = -204,
        ERR_CERT_UNABLE_TO_CHECK_REVOCATION = -205,
        ERR_CERT_REVOKED = -206,
        ERR_CERT_INVALID = -207,
        ERR_CERT_END = -208,
        ERR_INVALID_URL = -300,
        ERR_DISALLOWED_URL_SCHEME = -301,
        ERR_UNKNOWN_URL_SCHEME = -302,
        ERR_TOO_MANY_REDIRECTS = -310,
        ERR_UNSAFE_REDIRECT = -311,
        ERR_UNSAFE_PORT = -312,
        ERR_INVALID_RESPONSE = -320,
        ERR_INVALID_CHUNKED_ENCODING = -321,
        ERR_METHOD_NOT_SUPPORTED = -322,
        ERR_UNEXPECTED_PROXY_AUTH = -323,
        ERR_EMPTY_RESPONSE = -324,
        ERR_RESPONSE_HEADERS_TOO_BIG = -325,
        ERR_CACHE_MISS = -400,
        ERR_INSECURE_RESPONSE = -501,

    # Browser > GetImage(), RenderHandler > OnPaint().

    ctypedef enum cef_paint_element_type_t:
        PET_VIEW = 0,
        PET_POPUP,
    ctypedef cef_paint_element_type_t PaintElementType

    # Browser > SendMouseClickEvent().
    ctypedef enum cef_mouse_button_type_t:
        MBT_LEFT = 0,
        MBT_MIDDLE,
        MBT_RIGHT,
    ctypedef struct cef_mouse_event_t:
        int x
        int y
        uint32_t modifiers
    ctypedef cef_mouse_event_t CefMouseEvent

    # RenderHandler > GetScreenInfo():
    ctypedef struct cef_rect_t:
        int x
        int y
        int width
        int height
    ctypedef struct cef_screen_info_t:
        float device_scale_factor
        int depth
        int depth_per_component
        cpp_bool is_monochrome
        cef_rect_t rect
        cef_rect_t available_rect
    ctypedef cef_screen_info_t CefScreenInfo

    # CefURLRequest.GetStatus()
    ctypedef enum cef_urlrequest_status_t:
        UR_UNKNOWN = 0
        UR_SUCCESS
        UR_IO_PENDING
        UR_CANCELED
        UR_FAILED

    # CefJSDialogHandler.OnJSDialog()
    ctypedef enum cef_jsdialog_type_t:
        JSDIALOGTYPE_ALERT = 0,
        JSDIALOGTYPE_CONFIRM,
        JSDIALOGTYPE_PROMPT,
    ctypedef cef_jsdialog_type_t JSDIalogType

    # LifespanHandler and RequestHandler

    ctypedef enum cef_window_open_disposition_t:
        CEF_WOD_UNKNOWN,
        CEF_WOD_CURRENT_TAB,
        CEF_WOD_SINGLETON_TAB,
        CEF_WOD_NEW_FOREGROUND_TAB,
        CEF_WOD_NEW_BACKGROUND_TAB,
        CEF_WOD_NEW_POPUP,
        CEF_WOD_NEW_WINDOW,
        CEF_WOD_SAVE_TO_DISK,
        CEF_WOD_OFF_THE_RECORD,
        CEF_WOD_IGNORE_ACTION
    ctypedef cef_window_open_disposition_t WindowOpenDisposition

    ctypedef enum cef_path_key_t:
        PK_DIR_CURRENT,
        PK_DIR_EXE,
        PK_DIR_MODULE,
        PK_DIR_TEMP,
        PK_FILE_EXE,
        PK_FILE_MODULE,
        PK_LOCAL_APP_DATA,
        PK_USER_DATA,
        PK_DIR_RESOURCES,
    ctypedef cef_path_key_t PathKey

    # Drag & drop

    ctypedef enum cef_drag_operations_mask_t:
        DRAG_OPERATION_NONE    = 0
        DRAG_OPERATION_COPY    = 1
        DRAG_OPERATION_LINK    = 2
        DRAG_OPERATION_GENERIC = 4
        DRAG_OPERATION_PRIVATE = 8
        DRAG_OPERATION_MOVE    = 16
        DRAG_OPERATION_DELETE  = 32
        DRAG_OPERATION_EVERY   = UINT_MAX

    ctypedef enum cef_color_type_t:
        CEF_COLOR_TYPE_RGBA_8888,
        CEF_COLOR_TYPE_BGRA_8888,

    ctypedef enum cef_alpha_type_t:
        CEF_ALPHA_TYPE_OPAQUE,
        CEF_ALPHA_TYPE_PREMULTIPLIED,
        CEF_ALPHA_TYPE_POSTMULTIPLIED,

    ctypedef enum cef_focus_source_t:
        FOCUS_SOURCE_NAVIGATION,
        FOCUS_SOURCE_SYSTEM,

    cdef cppclass CefRange:
        uint32_t from_val "from"
        uint32_t to_val "to"

    # Download interrupt reasons.
    ctypedef enum cef_download_interrupt_reason_t:
        CEF_DOWNLOAD_INTERRUPT_REASON_NONE = 0
        CEF_DOWNLOAD_INTERRUPT_REASON_FILE_FAILED = 1
        CEF_DOWNLOAD_INTERRUPT_REASON_FILE_ACCESS_DENIED = 2
        CEF_DOWNLOAD_INTERRUPT_REASON_FILE_NO_SPACE = 3
        CEF_DOWNLOAD_INTERRUPT_REASON_FILE_NAME_TOO_LONG = 5
        CEF_DOWNLOAD_INTERRUPT_REASON_FILE_TOO_LARGE = 6
        CEF_DOWNLOAD_INTERRUPT_REASON_FILE_VIRUS_INFECTED = 7
        CEF_DOWNLOAD_INTERRUPT_REASON_FILE_TRANSIENT_ERROR = 10
        CEF_DOWNLOAD_INTERRUPT_REASON_FILE_BLOCKED = 11
        CEF_DOWNLOAD_INTERRUPT_REASON_FILE_SECURITY_CHECK_FAILED = 12
        CEF_DOWNLOAD_INTERRUPT_REASON_FILE_TOO_SHORT = 13
        CEF_DOWNLOAD_INTERRUPT_REASON_FILE_HASH_MISMATCH = 14
        CEF_DOWNLOAD_INTERRUPT_REASON_FILE_SAME_AS_SOURCE = 15
        CEF_DOWNLOAD_INTERRUPT_REASON_NETWORK_FAILED = 20
        CEF_DOWNLOAD_INTERRUPT_REASON_NETWORK_TIMEOUT = 21
        CEF_DOWNLOAD_INTERRUPT_REASON_NETWORK_DISCONNECTED = 22
        CEF_DOWNLOAD_INTERRUPT_REASON_NETWORK_SERVER_DOWN = 23
        CEF_DOWNLOAD_INTERRUPT_REASON_NETWORK_INVALID_REQUEST = 24
        CEF_DOWNLOAD_INTERRUPT_REASON_SERVER_FAILED = 30
        CEF_DOWNLOAD_INTERRUPT_REASON_SERVER_NO_RANGE = 31
        CEF_DOWNLOAD_INTERRUPT_REASON_SERVER_BAD_CONTENT = 33
        CEF_DOWNLOAD_INTERRUPT_REASON_SERVER_UNAUTHORIZED = 34
        CEF_DOWNLOAD_INTERRUPT_REASON_SERVER_CERT_PROBLEM = 35
        CEF_DOWNLOAD_INTERRUPT_REASON_SERVER_FORBIDDEN = 36
        CEF_DOWNLOAD_INTERRUPT_REASON_SERVER_UNREACHABLE = 37
        CEF_DOWNLOAD_INTERRUPT_REASON_SERVER_CONTENT_LENGTH_MISMATCH = 38
        CEF_DOWNLOAD_INTERRUPT_REASON_SERVER_CROSS_ORIGIN_REDIRECT = 39
        CEF_DOWNLOAD_INTERRUPT_REASON_USER_CANCELED = 40,
        CEF_DOWNLOAD_INTERRUPT_REASON_USER_SHUTDOWN = 41,
        CEF_DOWNLOAD_INTERRUPT_REASON_CRASH = 50
    ctypedef cef_download_interrupt_reason_t DownloadInterruptReason
