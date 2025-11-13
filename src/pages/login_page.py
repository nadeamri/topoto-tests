from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By


class LoginPage:
    # --- SÉLECTEURS CONFIRMÉS ---
    PAGE_TITLE = (By.XPATH, "//*[contains(text(), 'Connectez-vous')]")
    EMAIL_INPUT = (By.ID, "inputEmail")
    PASSWORD_INPUT = (By.ID, "inputPassword")
    LOGIN_BUTTON = (By.XPATH, "//button[@type='submit' and contains(@class, 'btn-danger')]")

    # NOUVEAU SÉLECTEUR DE SUCCÈS : Vérifie la présence de liens typiques de l'état "connecté"
    SUCCESS_ELEMENT_AFTER_LOGIN = (By.XPATH,
                                   "//a[normalize-space(text())='Mon Compte' or normalize-space(text())='Déconnexion' or contains(@href, '/profile') or contains(@class, 'user-menu-icon')]")

    # Message d'erreur (Utilisé par test_02)
    ERROR_MESSAGE = (By.XPATH, "//div[contains(@class, 'alert-danger') or contains(@class, 'alert-warning')]")
    # Anciens messages de succès (maintenant ignorés)
    SUCCESS_WELCOME_MESSAGE = (By.XPATH, "//h2[contains(text(), 'Bienvenue dans votre espace client')]")

    def __init__(self, driver):
        self.driver = driver

    def is_page_loaded(self, timeout=20):
        """Vérifie la présence des éléments de la page de connexion."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(self.PAGE_TITLE)
            )
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(self.EMAIL_INPUT)
            )
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(self.PASSWORD_INPUT)
            )
            return True
        except TimeoutException:
            return False

    def enter_credentials(self, email, password):
        """Saisit l'email et le mot de passe."""
        TIMEOUT = 10

        email_field = WebDriverWait(self.driver, TIMEOUT).until(
            EC.presence_of_element_located(self.EMAIL_INPUT)
        )
        email_field.clear()
        email_field.send_keys(email)

        password_field = WebDriverWait(self.driver, TIMEOUT).until(
            EC.presence_of_element_located(self.PASSWORD_INPUT)
        )
        password_field.clear()
        password_field.send_keys(password)

    def click_login(self):
        """Clique sur le bouton 'SE CONNECTER'."""
        login_btn = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.LOGIN_BUTTON)
        )
        login_btn.click()

    def login(self, email, password):
        """Méthode complète pour se connecter."""
        self.enter_credentials(email, password)
        self.click_login()

    def is_login_successful(self, timeout=10):
        """Vérifie la présence d'un élément dans la barre de navigation qui prouve la connexion."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(self.SUCCESS_ELEMENT_AFTER_LOGIN)
            )
            return True
        except TimeoutException:
            return False

    def is_error_message_displayed(self, timeout=5):
        """Vérifie si un message d'erreur est affiché (pour les identifiants invalides)."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(self.ERROR_MESSAGE)
            )
            return True
        except TimeoutException:
            return False

    def is_required_message_displayed(self, selector):
        """Vérifie si le navigateur bloque la soumission à cause d'un champ vide."""
        # ... (méthode inchangée, elle fonctionne)
        try:
            self.driver.find_element(*self.LOGIN_BUTTON)
            is_required = self.driver.execute_script(
                "return arguments[0].hasAttribute('required');",
                self.driver.find_element(*selector)
            )
            return is_required

        except Exception:
            return False