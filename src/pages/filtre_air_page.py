from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.by import By


class FiltreAirPage:
    # --- SÉLECTEURS ---
    PAGE_TITLE = (By.XPATH, "//*[normalize-space(text())='Filtre à Air']")
    AJOUTER_PANIER_BUTTON = (By.XPATH,
                             "(//button[contains(@class, 'btn-outline-danger') and normalize-space(text())='Ajouter au panier'])[1]")
    MODALE_CONTENEUR = (By.XPATH, "//div[contains(@class, 'modal-content')]")
    MODALE_TITRE = (By.XPATH, "//*[normalize-space(text())='Produit Ajouté au Panier']")

    # SÉLECTEUR MIS À JOUR : Ciblage direct et fiable par l'attribut href="/cart/" qui est unique pour le bouton de navigation vers le panier.
    VOIR_PANIER_BUTTON = (By.XPATH, "//a[@href='/cart/']")

    def __init__(self, driver):
        self.driver = driver

    def is_page_loaded(self, timeout=15):
        """Vérifie la présence du titre unique de la page pour confirmer le chargement."""
        print(f"Vérification du chargement de la page (attente max {timeout}s)...")
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(self.PAGE_TITLE)
            )
            return True
        except TimeoutException:
            return False

    def add_first_product_to_cart(self, timeout=15):
        print("Ajout du premier produit au panier...")

        try:
            # 1. Attendre que l'élément soit cliquable
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(self.AJOUTER_PANIER_BUTTON)
            )
            element.click()
            print("Clic standard réussi.")

        except (TimeoutException, ElementClickInterceptedException):
            print("Clic intercepté ou timeout. Tentative de clic forcé via JavaScript...")

            # Attendre de nouveau pour s'assurer que l'élément est dans le DOM
            element = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(self.AJOUTER_PANIER_BUTTON)
            )
            # Forcer le clic via JavaScript
            self.driver.execute_script("arguments[0].click();", element)
            print("Clic JavaScript exécuté.")

    def check_and_go_to_cart(self, timeout=10):
        """Vérifie la modale de confirmation et navigue vers le panier par JS."""
        print("Attente de la modale de confirmation (conteneur)...")

        # 1. Attendre que le CONTENEUR de la modale devienne visible
        WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(self.MODALE_CONTENEUR),
            message="Le conteneur de la modale n'est pas devenu visible."
        )

        # 2. Cliquer sur le bouton "Voir le panier" par JavaScript
        print("Modale trouvée et visible. Clic sur 'VOIR LE PANIER' par JavaScript...")

        # Le timeout reste à 10s pour plus de sécurité
        voir_panier = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.VOIR_PANIER_BUTTON),
            message="Le bouton 'VOIR LE PANIER' n'est pas trouvé dans le DOM."
        )
        self.driver.execute_script("arguments[0].click();", voir_panier)
        print("Clic JavaScript sur 'VOIR LE PANIER' exécuté.")