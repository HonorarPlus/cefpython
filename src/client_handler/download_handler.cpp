// Copyright (c) 2014 CEF Python, see the Authors file.
// All rights reserved. Licensed under BSD 3-clause license.
// Project website: https://github.com/cztomczak/cefpython

#include "download_handler.h"
#include "include/base/cef_logging.h"

bool DownloadHandler::CanDownload(CefRefPtr<CefBrowser> browser,
                    const CefString& url,
                    const CefString& request_method)
{
    REQUIRE_UI_THREAD();
    bool downloads_enabled = ApplicationSettings_GetBool("downloads_enabled");
    if (downloads_enabled) {
        auto msg = std::string{"[Browser process] Trying to download a file from: "};
        msg += url.ToString();
        LOG(INFO) << msg.c_str();
        return DownloadHandler_CanDownload(browser, url, request_method);
    } else {
        LOG(INFO) << "[Browser process] Tried to download file,"
                     " but downloads are disabled";
        return false;
    }
}


void DownloadHandler::OnBeforeDownload(
                            CefRefPtr<CefBrowser> browser,
                            CefRefPtr<CefDownloadItem> download_item,
                            const CefString& suggested_name,
                            CefRefPtr<CefBeforeDownloadCallback> callback)
{
    REQUIRE_UI_THREAD();
    bool downloads_enabled = ApplicationSettings_GetBool("downloads_enabled");
    if (downloads_enabled) {
        std::string msg = "[Browser process] About to download file: ";
        msg.append(suggested_name.ToString().c_str());
        LOG(INFO) << msg.c_str();
        DownloadHandler_OnBeforeDownload(browser, download_item, suggested_name, callback);
    } else {
        LOG(INFO) << "[Browser process] Tried to download file,"
                     " but downloads are disabled";
    }
}


void DownloadHandler::OnDownloadUpdated(
                                CefRefPtr<CefBrowser> browser,
                                CefRefPtr<CefDownloadItem> download_item,
                                CefRefPtr<CefDownloadItemCallback> callback)
{
    REQUIRE_UI_THREAD();
    DownloadHandler_OnDownloadUpdated(browser, download_item, callback);
    if (download_item->IsComplete()) {
        std::string msg = "[Browser process] Download completed, saved to: ";
        msg.append(download_item->GetFullPath().ToString().c_str());
        LOG(INFO) << msg.c_str();
    } else if (download_item->IsCanceled()) {
        LOG(INFO) << "[Browser process] Download was cancelled";
    }
}
