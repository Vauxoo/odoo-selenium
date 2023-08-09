"""Code to be used by testing suites"""
from os import environ
from resource import RLIMIT_AS, setrlimit
from typing import Dict, Union

from selenium.webdriver import Chrome, ChromeOptions, Remote
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait


class SeleniumMixin:
    """Provides startup code to correctly initialize Selenium.
    Test classes that wish to use it must inherit this class and explicitly call start/stop methods.
    Being a Mixin, this class needs to be first on the inheritance chain.
    """

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
        self.driver: Union[WebDriver, None] = None
        self.wait: Union[WebDriverWait, None] = None
        self._chrome_flags: Dict[str, str] = self._default_chrome_flags.copy()

    def start_selenium(self, flags: Union[Dict[str, str], None] = None):
        """Start Selenium"""
        # required to write updates to records so the frontend and backend is synced
        if env := getattr(self, "env"):
            if flush_all := getattr(env, "flush_all"):
                flush_all()  # odoo 16, flush() is deprecated
            else:
                env["base"].flush()

        if flags is not None:
            self._chrome_flags.update(flags)

        if grid_url := environ.get("SELENIUM_GRID_URL", False):
            self.driver = Remote(command_executor=grid_url, options=ChromeOptions())
        else:
            setrlimit(RLIMIT_AS, (16**9, 16**9))

            options = Options()
            for key, value in self._chrome_flags.items():
                options.add_argument(f"{key}={value}" if value else key)

            self.driver = Chrome(
                service=Service(),
                options=options,
            )

        timeout = environ.get("SELENIUM_TIMEOUT", 300)
        self.wait = WebDriverWait(self.driver, timeout=timeout, poll_frequency=1)
        self.driver.implicitly_wait(timeout)

    def stop_selenium(self):
        """Stop Selenium"""
        # required to prevent 'cursor already closed' errors on teardown
        if callable(wait_for_requests := getattr(self, "_wait_remaining_requests")):
            wait_for_requests()
        self.driver.quit()
