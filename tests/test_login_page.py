import pytest
from src.pages.login_page import LoginPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Identifiants valides (À REMPLACER PAR LES VRAIS SI NÉCESSAIRE)
VALID_EMAIL = "aamrinada489@gmail.com"
VALID_PASSWORD = "nada123"


class TestLogin:

    @pytest.fixture(autouse=True)
    def setup_method(self, driver):
        """Ouvre la page de connexion avant chaque test.
        Inclut l'attente pour le préchargeur et le changement d'URL."""

        # 1. Naviguer vers la page d'accueil
        driver.get("https://topoto.tn/")

        # 2. Attendre que le préchargeur disparaisse
        preloader_locator = (By.CLASS_NAME, "preloader-wapper")
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located(preloader_locator),
            "Timeout: Le préchargeur a mis trop de temps à disparaître."
        )

        # Enregistrer l'URL actuelle (la page d'accueil)
        initial_url = driver.current_url

        # 3. Cliquer sur "SE CONNECTER" dans la barre de navigation
        connect_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[normalize-space(text())='Se connecter']"))
        )
        connect_button.click()

        # Attendre que l'URL change (navigation vers la page de login)
        WebDriverWait(driver, 10).until(
            EC.url_changes(initial_url),
            "Timeout: Le navigateur n'a pas navigué vers la page de connexion."
        )

        # 4. Initialiser la Page Object et vérifier le chargement de la page de login
        self.login_page = LoginPage(driver)
        assert self.login_page.is_page_loaded(), "La page de connexion n'a pas été chargée."

    def test_01_successful_login(self, driver):
        """Scénario 1: Connexion avec des identifiants valides."""
        print("\n--- TEST: Connexion Réussie ---")

        self.login_page.login(VALID_EMAIL, VALID_PASSWORD)

        # 1. Vérification du succès (élément de profil/déconnexion)
        assert self.login_page.is_login_successful(), "ÉCHEC: La connexion a échoué. L'élément de profil/déconnexion n'est pas apparu sur la page d'accueil."

        # 2. Vérification de la redirection vers l'accueil (comme confirmé par l'utilisateur)
        expected_url = "https://topoto.tn/"
        # Utilisation de rstrip('/') pour gérer la barre oblique finale si elle est absente dans l'URL actuelle
        assert driver.current_url.rstrip('/') == expected_url.rstrip(
            '/'), f"ÉCHEC: Redirection vers l'URL inattendue: {driver.current_url}. Attendue: {expected_url}"

        print(f"SUCCÈS: Connexion réussie et redirection vers la page d'accueil confirmée.")

    def test_02_invalid_credentials(self, driver):
        """Scénario 2: Connexion avec mot de passe invalide."""
        print("\n--- TEST: Identifiants Invalides (Mot de passe) ---")

        INVALID_PASSWORD = "mauvaismotdepasse"

        self.login_page.login(VALID_EMAIL, INVALID_PASSWORD)

        # Vérification de l'affichage du message d'erreur
        assert self.login_page.is_error_message_displayed(), "ÉCHEC: Aucun message d'erreur affiché pour un mot de passe invalide."
        print("SUCCÈS: Message d'erreur affiché pour les identifiants invalides.")

    def test_03_empty_email_field(self, driver):
        """Scénario 3: Tentative de connexion avec le champ Email vide."""
        print("\n--- TEST: Champ Email Vide ---")

        self.login_page.login("", VALID_PASSWORD)

        # Vérification que la page n'a PAS changé après le clic (validation HTML5)
        assert self.login_page.is_page_loaded(
            timeout=2), "ÉCHEC: La page a changé, la soumission a réussi de manière inattendue."

        # Vérification que le navigateur applique la contrainte 'required' sur le champ email
        assert self.login_page.is_required_message_displayed(self.login_page.EMAIL_INPUT), \
            "ÉCHEC: Le formulaire a soumis ou le champ email n'a pas la contrainte 'required'."
        print("SUCCÈS: La soumission est bloquée pour le champ Email vide (validation HTML5).")

    def test_04_empty_password_field(self, driver):
        """Scénario 4: Tentative de connexion avec le champ Mot de passe vide."""
        print("\n--- TEST: Champ Mot de passe Vide ---")

        self.login_page.login(VALID_EMAIL, "")

        # Vérification que la page n'a PAS changé après le clic
        assert self.login_page.is_page_loaded(
            timeout=2), "ÉCHEC: La page a changé, la soumission a réussi de manière inattendue."

        # Vérification que le navigateur applique la contrainte 'required' sur le champ mot de passe
        assert self.login_page.is_required_message_displayed(self.login_page.PASSWORD_INPUT), \
            "ÉCHEC: Le formulaire a soumis ou le champ Mot de passe n'a pas la contrainte 'required'."
        print("SUCCÈS: La soumission est bloquée pour le champ Mot de passe vide (validation HTML5).")