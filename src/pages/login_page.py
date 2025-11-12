from src.pages.base_page import BasePage
from selenium.webdriver.common.by import By

class LoginPage(BasePage):
    EMAIL_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "password")
    SUBMIT_BUTTON = (By.XPATH, "//button[@type='submit']")

    def login(self, email, password):
        self.fill(self.EMAIL_INPUT, email)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.SUBMIT_BUTTON)
