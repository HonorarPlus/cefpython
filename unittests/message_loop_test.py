# Copyright (c) 2016 CEF Python, see the Authors file.
# All rights reserved. Licensed under BSD 3-clause license.
# Project website: https://github.com/cztomczak/cefpython

"""Verify that closing a top-level browser exits the native message loop."""

import os
import shutil
import tempfile
import threading
import unittest

import _test_runner
from cefpython3 import cefpython as cef


class MessageLoop_IsolatedTest(unittest.TestCase):

    def test_top_level_browser_close_quits_message_loop(self):
        cache_path = tempfile.mkdtemp(prefix="cefpython-message-loop-")
        browser_closed = threading.Event()
        timeout_reached = threading.Event()
        browser = None

        try:
            cef.Initialize(settings={
                    "cache_path": cache_path,
                    "remote_debugging_port": -1,
            })
            browser = cef.CreateBrowserSync(
                    url="data:text/html,<h1>Message loop test</h1>",
                    window_title="CEF message loop test")
            browser.SetClientHandler(
                    LifespanHandler(browser_closed))

            close_timer = threading.Timer(
                    0.5, browser.CloseBrowser, args=(True,))
            close_timer.daemon = True
            close_timer.start()

            def stop_hung_test():
                timeout_reached.set()
                cef.QuitMessageLoop()

            timeout_timer = threading.Timer(10.0, stop_hung_test)
            timeout_timer.daemon = True
            timeout_timer.start()

            cef.MessageLoop()

            close_timer.cancel()
            timeout_timer.cancel()
            self.assertFalse(
                    timeout_reached.is_set(),
                    "Timed out waiting for the top-level browser to close")
            self.assertTrue(browser_closed.is_set())
        finally:
            browser = None
            cef.Shutdown()
            shutil.rmtree(cache_path, ignore_errors=True)


class LifespanHandler(object):

    def __init__(self, browser_closed):
        self.browser_closed = browser_closed

    def OnBeforeClose(self, browser):
        self.browser_closed.set()


if __name__ == "__main__":
    _test_runner.main(os.path.basename(__file__))
