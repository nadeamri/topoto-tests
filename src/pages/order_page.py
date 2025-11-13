from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.expected_conditions import url_contains
import time
import re  # Import nécessaire pour l'extraction par expression régulière


class OrderPage:
    # --- SÉLECTEURS DU FORMULAIRE (INCHANGÉS) ---
    PAGE_TITLE = (By.XPATH, "//*[normalize-space(text())='Créer une Nouvelle Commande']")
    INPUT_NOM = (By.NAME, "order[nom]")
    INPUT_PRENOM = (By.NAME, "order[prenom]")
    INPUT_EMAIL = (By.NAME, "order[email]")
    INPUT_TELEPHONE = (By.NAME, "order[telephone]")
    RADIO_RETRAIT_MAGASIN = (By.XPATH,
                             "//label[normalize-space(text())='Retrait au magasin']/preceding-sibling::input[@type='radio']")
    CONFIRM_ORDER_BUTTON = (By.ID, "order_submit")

    # --- SÉLECTEUR DE LA PAGE DE CONFIRMATION (CORRIGÉ) ---
    # Nous ciblons maintenant le bloc de texte qui contient l'étiquette "Référence :".
    REFERENCE_LOCATOR = (By.XPATH, "//*[contains(text(), 'Référence :') or contains(., 'Référence :')]")

    def __init__(self, driver):
        self.driver = driver

    def is_order_form_loaded(self, timeout=10):
        """Vérifie la présence du champ Nom sur la page de commande."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(self.INPUT_NOM)
            )
            return True
        except TimeoutException:
            return False

    def fill_order_form(self, nom, prenom, email, telephone):
        """Remplir le formulaire de commande et sélectionner le retrait au magasin."""
        TIMEOUT = 10

        WebDriverWait(self.driver, TIMEOUT).until(
            EC.visibility_of_element_located(self.INPUT_NOM)
        ).send_keys(nom)

        self.driver.find_element(*self.INPUT_PRENOM).send_keys(prenom)
        self.driver.find_element(*self.INPUT_EMAIL).send_keys(email)
        self.driver.find_element(*self.INPUT_TELEPHONE).send_keys(telephone)

        retrait_radio = WebDriverWait(self.driver, TIMEOUT).until(
            EC.element_to_be_clickable(self.RADIO_RETRAIT_MAGASIN)
        )
        retrait_radio.click()

    def confirm_order(self):
        """Clique sur le bouton 'Confirmer la commande' en utilisant JS pour la robustesse."""

        confirm_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.CONFIRM_ORDER_BUTTON)
        )

        print("Tentative de clic robuste sur 'Confirmer la commande'...")

        try:
            # 1. Défilement pour s'assurer que l'élément est dans la zone visible
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", confirm_btn)
            time.sleep(0.5)

            # 2. Clic JavaScript forcé
            self.driver.execute_script("arguments[0].click();", confirm_btn)
            print("[OK] Confirmation de la commande cliquée avec succès via JavaScript.")

        except Exception as e:
            print(f"Échec critique du clic JavaScript: {e}")
            raise

    def is_order_confirmed(self, timeout=15):
        """
        ✅ VÉRIFICATION CORRIGÉE : Vérifie que l'URL contient '/order/confirmation/'.
        """
        print("Vérification de la redirection vers la page de confirmation...")
        try:
            WebDriverWait(self.driver, timeout).until(
                url_contains("/order/confirmation/")
            )
            return True
        except TimeoutException:
            return False

    def get_confirmation_reference(self, timeout=5):
        """
        ✅ CORRECTION APPLIQUÉE : Récupère l'élément parent et utilise regex pour extraire le numéro de référence.
        """
        try:
            reference_element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(self.REFERENCE_LOCATOR)
            )

            full_text = reference_element.text

            # Recherche de la référence: 'Référence : ' suivi d'un groupe de caractères (chiffres/lettres)
            match = re.search(r'Référence :\s*([\w\d]+)', full_text, re.IGNORECASE)

            if match:
                reference = match.group(1).strip()
                print(f"✅ Référence trouvée par parsing: {reference}")
                return reference
            else:
                print(f"❌ Erreur: Référence non trouvée dans le texte: '{full_text}'")
                return None

        except TimeoutException:
            print(f"❌ Erreur: L'élément de référence n'a pas été trouvé avec le sélecteur: {self.REFERENCE_LOCATOR[1]}")
            return None
