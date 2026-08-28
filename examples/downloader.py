# Downloader example. Doesn't depend on any third party GUI framework.
# Tested with CEF Python v108.4.

from cefpython3 import cefpython as cef
import platform
import sys


def main():
    check_versions()
    sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error

    settings = {
        'downloads_enabled' : True
    }

    cef.Initialize(settings=settings)

    browser = cef.CreateBrowserSync(url="https://www.putty.org/", window_title="Downloader test")

    browser.SetClientHandler(DownloadHandler())
    cef.MessageLoop()
    cef.Shutdown()

class DownloadHandler(object):

    def CanDownload(self, browser, url, request_method):
        print("Checking if url {} can be downloaded".format(url))
        browser.StartDownload(url)

    def OnBeforeDownload(self, browser, download_item, suggested_name, callback):
        print("Downloading: {}".format(suggested_name))
        callback.Continue(suggested_name, True)


    def OnDownloadUpdated(self, browser, download_item, callback):
        print("Download update {}".format(download_item.GetPercentComplete()))
        if download_item.IsComplete():
            print("Download finished")
            print("Full path: {}".format(download_item.GetFullPath()))



def check_versions():
    ver = cef.GetVersion()
    print("[hello_world.py] CEF Python {ver}".format(ver=ver["version"]))
    print("[hello_world.py] Chromium {ver}".format(ver=ver["chrome_version"]))
    print("[hello_world.py] CEF {ver}".format(ver=ver["cef_version"]))
    print("[hello_world.py] Python {ver} {arch}".format(
           ver=platform.python_version(),
           arch=platform.architecture()[0]))
    assert float(cef.__version__) >= 108.4, "CEF Python v108.4+ required to run this"

if __name__ == '__main__':
    main()
