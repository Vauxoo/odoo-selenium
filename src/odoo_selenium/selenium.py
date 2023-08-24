"""Code to be used by testing suites"""
from __future__ import annotations

import logging
from os import environ
from resource import RLIMIT_AS, setrlimit

from selenium.webdriver import Chrome, ChromeOptions, Remote
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

from odoo_selenium.expectations import owl_has_loaded

try:
    from odoo.tools import config
except ImportError:
    config = {"http_port": 8069}

_logger = logging.getLogger(__name__)


class SeleniumMixin:
    """Provides startup code to correctly initialize Selenium.
    Test classes that wish to use it must inherit this class and explicitly call start/stop methods.
    Being a Mixin, this class needs to be first on the inheritance chain.
    """

    odoo_url = environ.get("SELENIUM_BASE_URL", f"http://127.0.0.1:{config['http_port']}")
    _default_chrome_flags = {
        "--headless": "",
        "--no-default-browser-check": "",
        "--no-first-run": "",
        "--disable-extensions": "",
        "--disable-background-networking": "",
        "--disable-background-timer-throttling": "",
        "--disable-backgrounding-occluded-windows": "",
        "--disable-renderer-backgrounding": "",
        "--disable-breakpad": "",
        "--disable-client-side-phishing-detection": "",
        "--disable-crash-reporter": "",
        "--disable-default-apps": "",
        "--disable-dev-shm-usage": "",
        "--disable-device-discovery-notifications": "",
        "--disable-namespace-sandbox": "",
        "--disable-translate": "",
        "--autoplay-policy": "no-user-gesture-required",
        "--window-size": "1376,768",
        "--no-sandbox": "",
        "--disable-gpu": "",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.driver: WebDriver | None = None
        self.wait: WebDriverWait | None = None
        self.selenium_timeout: float = environ.get("SELENIUM_TIMEOUT", 300.0)
        self._chrome_flags: dict[str, str] = self._default_chrome_flags.copy()

    def start_selenium(self, flags: dict[str, str] | None = None):
        """Start Selenium"""
        # required to write updates to records so the frontend and backend is synced
        try:
            self.env.flush_all()  # odoo 16, flush() is deprecated
        except AttributeError:
            try:
                self.env["base"].flush()
            except (AttributeError, KeyError):
                _logger.warning("Failed to flush, changes may not be reflected on the website")

        grid_url = environ.get("SELENIUM_GRID_URL", False)
        if grid_url:
            self.driver = Remote(command_executor=grid_url, options=ChromeOptions())
        else:
            if flags is not None:
                self._chrome_flags.update(flags)

            setrlimit(RLIMIT_AS, (16**9, 16**9))

            options = Options()
            for key, value in self._chrome_flags.items():
                options.add_argument(f"{key}={value}" if value else key)

            self.driver = Chrome(
                service=Service(),
                options=options,
            )

        self.wait = WebDriverWait(self.driver, timeout=self.selenium_timeout, poll_frequency=1)
        self.driver.implicitly_wait(self.selenium_timeout)

    def stop_selenium(self):
        """Stop Selenium"""
        # required to prevent 'cursor already closed' errors on teardown
        try:
            self._wait_remaining_requests()
        except AttributeError:
            _logger.warning("Failed to call _wait_remaining_requests, is this an HttpCase?")

        self.driver.quit()

    def navigate(self, url: str):
        """Navigates to the specified Odoo website and waits for the website components to load.

        :param str url: URL to navigate to. It MUST be an Odoo website, otherwise it is likely to wait indefinitely
        for Odoo specific components (that are not there) to load.
        """
        self.driver.get(url)
        self.wait.until(owl_has_loaded)
