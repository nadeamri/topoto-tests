from src.pages.base_page import BasePage
from selenium.webdriver.common.by import By

class ContactPage(BasePage):
    CONTACT_FORM = (By.ID, "contact-form")
    NAME_INPUT = (By.NAME, "name")
    EMAIL_INPUT = (By.NAME, "email")
    MESSAGE_INPUT = (By.NAME, "message")
    SUBMIT_BUTTON = (By.XPATH, "//button[@type='submit']")

    def send_message(self, name, email, message):
        self.fill(self.NAME_INPUT, name)
        self.fill(self.EMAIL_INPUT, email)
        self.fill(self.MESSAGE_INPUT, message)
        self.click(self.SUBMIT_BUTTON)
