from src.pages.base_page import BasePage
from selenium.webdriver.common.by import By

class HomePage(BasePage):
    URL = "https://topoto.tn/"

    LOGIN_BUTTON = (By.XPATH, "//a[contains(@href, 'login')]")
    CONTACT_LINK = (By.XPATH, "//a[contains(text(), 'Contact')]")

    def open_home_page(self):
        self.open(self.URL)

    def go_to_login(self):
        self.click(self.LOGIN_BUTTON)

    def go_to_contact(self):
        self.click(self.CONTACT_LINK)
