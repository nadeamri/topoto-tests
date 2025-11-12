from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.by import By


class CartPage:
    # --- SÉLECTEURS ---
    PAGE_TITLE = (By.XPATH, "//*[normalize-space(text())='Votre Panier']")

    # Sélecteur pour la ligne contenant le produit (insensible à la casse des accents)
    ROW_PRODUIT = (By.XPATH,
                   "//table[contains(@class, 'table')]//tr[contains(translate(., 'abcdefghijklmnopqrstuvwxyzàâéèêëîïôœùûüÿç', 'ABCDEFGHIJKLMNOPQRSTUVWXYZÀÂÉÈÊËÎÏÔŒÙÛÜŸÇ'), 'FILTRE À AIR')]")

    # SÉLECTEUR MIS À JOUR : Ciblage par la classe 'btn-danger' ET vérification si l'élément contient le texte 'Retirer' (insensible à la casse).
    # Cela gère la présence de l'icône <i> et assure que l'élément est trouvé.
    REMOVE_BUTTON = (By.XPATH,
                     "//a[contains(@class, 'btn-danger') and contains(translate(., 'retirer', 'RETIRER'), 'RETIRER')]")

    def __init__(self, driver):
        self.driver = driver

    def is_page_loaded(self, timeout=15):
        """Vérifie la présence du titre de la page du panier."""
        print(f"Vérification du chargement de la page panier (attente max {timeout}s)...")
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(self.PAGE_TITLE)
            )
            return True
        except TimeoutException:
            return False

    def is_product_in_cart(self, timeout=10):
        """Vérifie la présence du produit dans le tableau du panier."""
        print("Vérification de la présence du produit dans le panier...")
        # Attendre le chargement de la page du panier avant de chercher l'élément
        if not self.is_page_loaded(timeout=5):
            print("Erreur: La page du panier n'a pas été chargée correctement.")
            return False

        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(self.ROW_PRODUIT)
            )
            return True
        except TimeoutException:
            print("Erreur: Le produit n'a pas été trouvé dans le panier.")
            return False

    def remove_product_from_cart(self, timeout=10):
        """Clique sur le bouton 'RETIRER' pour nettoyer le panier."""
        print("Tentative de retrait du produit du panier...")
        try:
            # Attendre que le bouton 'RETIRER' soit cliquable
            remove_btn = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(self.REMOVE_BUTTON),
                message="Le bouton de retrait n'est pas cliquable."
            )
            # Cliquer sur le bouton
            remove_btn.click()
            print("Produit retiré avec succès.")

        except TimeoutException as e:
            # Si le timeout se produit, afficher l'erreur pour le débogage.
            print(f"Erreur Timeout lors du retrait: {e.msg}")
            raise  # Renvoyer l'exception pour marquer l'étape de nettoyage comme échouée
        except Exception as e:
            print(f"Erreur inattendue lors du retrait: {e}")
            raise  # Renvoyer l'exception
