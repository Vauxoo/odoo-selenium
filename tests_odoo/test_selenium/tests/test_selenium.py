from selenium.webdriver.common.by import By

from odoo.tests import HttpCase, tagged

from osut.selenium import SeleniumMixin


@tagged("-at_install", "post_install")
class TestSelenium(SeleniumMixin, HttpCase):
    def setUp(self):
        super().setUp()
        self.start_selenium()

    def tearDown(self):
        super().tearDown()
        self.stop_selenium()

    def test_login_page(self):
        self.driver.get(f"{self.base_url()}/web/login")
        email_input = self.driver.find_element(By.ID, "login")

        self.assertEqual("Email", email_input.get_attribute("placeholder"))
