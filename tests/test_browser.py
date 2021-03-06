import tempfile
import shutil
import os
from selenium import webdriver
import bok_choy.browser
from unittest import TestCase
from mock import patch

from .pages import ButtonPage


class TestBrowser(TestCase):

    @patch.dict(os.environ, {'SELENIUM_BROWSER': 'firefox'})
    def test_local_browser(self):
        browser = bok_choy.browser.browser()
        self.addCleanup(browser.quit)
        self.assertIsInstance(browser, webdriver.Firefox)

    @patch.dict(os.environ, {'SELENIUM_BROWSER': 'invalid'})
    def test_invalid_browser_name(self):
        with self.assertRaises(bok_choy.browser.BrowserConfigError):
            bok_choy.browser.browser()

    def test_save_screenshot(self):

        # Create a temp directory to save the screenshot to
        tempdir_path = tempfile.mkdtemp()
        self.addCleanup(lambda: shutil.rmtree(tempdir_path))

        # Configure the screenshot directory using an environment variable
        os.environ['SCREENSHOT_DIR'] = tempdir_path

        # Take a screenshot of a page
        browser = bok_choy.browser.browser()
        self.addCleanup(browser.quit)

        ButtonPage(browser).visit()
        bok_choy.browser.save_screenshot(browser, 'button_page')

        # Check that the file was created
        expected_file = os.path.join(tempdir_path, 'button_page.png')
        self.assertTrue(os.path.isfile(expected_file))

        # Check that the file is not empty
        self.assertGreater(os.stat(expected_file).st_size, 100)
