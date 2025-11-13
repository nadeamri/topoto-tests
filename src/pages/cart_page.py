from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By


class CartPage:
    # --- SÉLECTEURS ---
    PAGE_TITLE = (By.XPATH, "//*[normalize-space(text())='Votre Panier']")

    # ✅ CORRIGÉ: SÉLECTEUR GÉNÉRIQUE DE DERNIER RECOURS
    # Recherche la première ligne <tr> dans le corps de la table.
    # Si le panier n'est pas vide, cette ligne doit exister.
    ROW_PRODUIT = (By.XPATH,
                   "//table[contains(@class, 'table')]//tbody//tr[1]")

    # SÉLECTEUR RETIRER
    REMOVE_BUTTON = (By.XPATH,
                     "//a[contains(@class, 'btn-danger') and contains(translate(., 'retirer', 'RETIRER'), 'RETIRER')]")

    # ✅ OPTIMISÉ: Cible l'ancre <a href="/order/new"> spécifique du bouton "Commander"
    COMMANDER_BUTTON = (By.XPATH,
                        "//a[@href='/order/new' and contains(translate(., 'commander', 'COMMANDER'), 'COMMANDER')]")

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
        """Vérifie la présence du produit dans le tableau du panier (utilise le sélecteur générique)."""
        print("Vérification de la présence du produit dans le panier...")
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
            remove_btn = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(self.REMOVE_BUTTON),
                message="Le bouton de retrait n'est pas cliquable."
            )
            remove_btn.click()
            print("Produit retiré avec succès.")

        except TimeoutException as e:
            print(f"Erreur Timeout lors du retrait: {e.msg}")
            raise
        except Exception as e:
            print(f"Erreur inattendue lors du retrait: {e}")
            raise

    def click_commander_button(self, timeout=10):
        """Clique sur le bouton 'Commander' pour passer commande (avec fallback JS)."""
        print("Clic sur le bouton 'Commander'...")
        try:
            button = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(self.COMMANDER_BUTTON)
            )
            button.click()
            print("[OK] Bouton 'Commander' cliqué avec succès.")
        except Exception:
            # Fallback JavaScript si le clic normal échoue
            print("Tentative de clic JavaScript...")
            button = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(self.COMMANDER_BUTTON)
            )
            self.driver.execute_script("arguments[0].click();", button)
            print("[OK] Bouton 'Commander' cliqué via JavaScript")