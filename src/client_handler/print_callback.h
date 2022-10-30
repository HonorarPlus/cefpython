#pragma once
#include "common/cefpython_public_api.h"


class PdfPrintCallback : public CefPdfPrintCallback
{
  public:
    PdfPrintCallback(CefRefPtr<CefBrowser> browser)
        : browser_(browser) {}
    virtual void OnPdfPrintFinished(const CefString& path, bool ok) override;

  protected:
    CefRefPtr<CefBrowser> browser_;
    IMPLEMENT_REFCOUNTING(PdfPrintCallback);
};
