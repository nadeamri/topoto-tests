from selenium.webdriver.common.by import By

class BasePage:
    """Classe de base pour toutes les pages du site."""
    def __init__(self, driver):
        self.driver = driver

    def open(self, url):
        self.driver.get(url)

    def click(self, locator):
        self.driver.find_element(*locator).click()

    def fill(self, locator, text):
        element = self.driver.find_element(*locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        return self.driver.find_element(*locator).text

    def get_title(self):
        return self.driver.title