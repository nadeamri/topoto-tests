# Dans src/pages/product_page.py
# Assurez-vous que les imports nécessaires sont présents
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
# ...

class ProductPage:
    # URL de la page produits
    URL = "https://topoto.tn/product/shop"

    FILTRE_AIR_LINK = (By.XPATH, "//a[contains(@href, 'subcategory/5')]")

    def __init__(self, driver):
        self.driver = driver

    def open_product_page(self):
        self.driver.get(self.URL)

    def click_filtre_air_link(self, timeout=15):
        print("Attente de la présence de l'élément 'Filtre à Air'...")
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(self.FILTRE_AIR_LINK)
            )
        except TimeoutException as e:
            # Si l'élément n'apparaît pas du tout dans le DOM, le test doit échouer ici.
            print(f"Échec critique: L'élément 'Filtre à Air' n'est pas présent dans le DOM après {timeout}s.")
            raise e

        print("Élément trouvé. Forçage du clic via JavaScript...")
        self.driver.execute_script("arguments[0].click();", element)