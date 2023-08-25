from selenium.webdriver.common.by import By

from odoo.tests import tagged

from odoo_selenium import SeleniumCase


@tagged("-at_install", "post_install")
class TestSelenium(SeleniumCase):
    def test_login_page(self):
        self.navigate("/web/login")
        email_input = self.driver.find_element(By.ID, "login")

        self.assertEqual("Email", email_input.get_attribute("placeholder"))
