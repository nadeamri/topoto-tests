from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time  # ✅ AJOUTÉ: Nécessaire pour le sleep après scroll et navigation


class FiltreAirPage:
    # --- SÉLECTEURS ---
    # Sélecteur de titre de page plus robuste
    PAGE_TITLE_HEADER = (By.XPATH,
                         "//h1[normalize-space(text())='Filtre à Air'] | //h2[normalize-space(text())='Filtre à Air']")

    # Bouton 'Ajouter au panier'
    ADD_TO_CART_BUTTON = (By.XPATH,
                          "//button[contains(@class, 'btn-outline-danger') and normalize-space(text())='Ajouter au panier']")

    # Bouton 'Voir le panier' dans la modale d'ajout
    VIEW_CART_BUTTON_MODAL = (By.XPATH,
                              "//a[contains(@class, 'btn-danger') and normalize-space(text())='Voir le panier']")

    def __init__(self, driver):
        self.driver = driver

    def is_page_loaded(self, timeout=15):
        """Vérifie que la page 'Filtre à Air' est bien chargée en cherchant le titre H1/H2."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(self.PAGE_TITLE_HEADER)
            )
            return True
        except TimeoutException:
            # Fallback (vérification du titre de la fenêtre)
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.title_contains("Filtre à Air")
                )
                return True
            except TimeoutException:
                return False

    def add_first_product_to_cart(self):
        """Clique sur le premier bouton 'Ajouter au panier' en utilisant JS pour la robustesse."""

        add_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.ADD_TO_CART_BUTTON)
        )

        print("Tentative de clic robuste sur 'Ajouter au panier'...")

        # 1. Défilement pour s'assurer que l'élément est dans la zone visible
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_btn)
        time.sleep(0.5)

        # 2. Clic JavaScript forcé
        self.driver.execute_script("arguments[0].click();", add_btn)
        print("[OK] Ajout au panier cliqué avec succès via JavaScript.")

    def check_and_go_to_cart(self):
        """Attend la modale et clique sur 'Voir le panier'."""
        print("Attente du bouton 'Voir le panier'...")
        view_cart_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.VIEW_CART_BUTTON_MODAL)
        )

        # Utilisation de JS pour cliquer pour plus de fiabilité sur la modale
        self.driver.execute_script("arguments[0].click();", view_cart_btn)

        # ✅ AJOUTÉ: Pause pour attendre la redirection et le chargement AJAX du produit dans le panier
        time.sleep(1)

        print("[OK] Navigation vers le panier après l'ajout.")