"""Collection of useful expectations to be used with Selenium waits"""
from selenium.common import JavascriptException
from selenium.webdriver.remote.webdriver import WebDriver


def owl_has_loaded(driver: WebDriver) -> bool:
    """An expectation for Odoo's OWL framework to have finished loading.

    :param WebDriver driver: Driver that has navigated to an Odoo website and expects OWL to have loaded.
    :return: True if OWL has loaded, False otherwise.
    """
    try:
        return driver.execute_script("return typeof owl.config.mode !== 'undefined'")
    except JavascriptException:
        try:
            return driver.execute_script(
                "return Array.from(__OWL_DEVTOOLS__.apps).some((app) => app.root?.status === 1)"
            )
        except JavascriptException:
            return False
