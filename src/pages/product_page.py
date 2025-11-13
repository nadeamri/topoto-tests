from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import TimeoutException


class ProductPage:
    # --- SÉLECTEURS ---
    NAV_PRODUITS = (By.XPATH, "//a[@href='/product/shop']")
    NAV_FILTRE_A_AIR = (By.XPATH, "//a[@href='/product/subcategory/5']")

    # Sélecteurs de vérification (pour d'autres tests)
    PRODUCTS_TITLE = (By.XPATH, "//h2[normalize-space(text())='Nos produits']")
    CATEGORIES_TITLE = (By.XPATH, "//h2[normalize-space(text())='Nos Catégories']")
    VIDANGE_PRODUCT = (By.XPATH, "//a[contains(text(), 'VIDANGE')]")

    def __init__(self, driver):
        self.driver = driver
        self.BASE_URL = "https://topoto.tn/"

    def open_product_page(self):
        """Ouvre la page d'accueil, attend le préchargeur, et clique sur 'Produits'."""
        self.driver.get(self.BASE_URL)

        # Attente du préchargeur
        preloader_locator = (By.CLASS_NAME, "preloader-wapper")
        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located(preloader_locator),
            "Timeout: Le préchargeur a mis trop de temps à disparaître."
        )

        # Clic sur le lien 'Produits'
        produits_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.NAV_PRODUITS)
        )
        produits_btn.click()

    def click_filtre_air_link(self):
        """Clique sur le lien 'Filtre à Air' en utilisant le scroll et JS pour la robustesse."""
        filtre_air_link = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.NAV_FILTRE_A_AIR)
        )

        # Défilement (scroll) pour amener l'élément en vue
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", filtre_air_link)
        time.sleep(0.5)

        # Clic JavaScript forcé
        self.driver.execute_script("arguments[0].click();", filtre_air_link)

    # --- Méthodes de vérification ---
    def get_products_title(self):
        return WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.PRODUCTS_TITLE)).text

    def get_categories_title(self):
        return WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.CATEGORIES_TITLE)).text

    def is_vidange_displayed(self):
        try:
            return WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(self.VIDANGE_PRODUCT)).is_displayed()
        except TimeoutException:
            return False