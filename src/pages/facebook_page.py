from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By


class FacebookPage:
    """Page Object pour la page Facebook"""

    def __init__(self, driver):
        self.driver = driver

    def is_facebook_page_loaded(self, timeout=15):
        """Vérifie que la page Facebook est chargée."""
        print(f"Verification du chargement de la page Facebook (attente max {timeout}s)...")
        try:
            # Vérifier l'URL
            current_url = self.driver.current_url.lower()
            print(f"[INFO] URL actuelle: {current_url}")

            # Vérifier si on est sur Facebook
            if "facebook.com" in current_url or "fb.com" in current_url:
                print("[OK] On est sur la page Facebook")
                return True

            # Vérifier la présence d'éléments typiques de Facebook
            facebook_indicators = [
                (By.XPATH, "//a[contains(@href, 'facebook.com')]"),
                (By.XPATH, "//*[contains(@id, 'facebook')]"),
                (By.XPATH, "//*[contains(@class, 'facebook')]"),
                (By.XPATH, "//*[contains(text(), 'Facebook')]")
            ]

            for indicator in facebook_indicators:
                try:
                    WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located(indicator)
                    )
                    print("[OK] Element Facebook trouve")
                    return True
                except TimeoutException:
                    continue

            return False
        except Exception as e:
            print(f"[INFO] Erreur lors de la verification: {e}")
            return False

    def get_facebook_url(self):
        """Récupère l'URL actuelle de Facebook."""
        return self.driver.current_url

    def is_facebook_page_accessible(self, timeout=10):
        """Vérifie si la page Facebook est accessible."""
        try:
            # Vérifier le titre de la page
            page_title = self.driver.title.lower()
            print(f"[INFO] Titre de la page: {self.driver.title}")

            # Vérifier que le titre contient Facebook ou Topoto
            if "facebook" in page_title or "topoto" in page_title:
                print("[OK] Titre de la page valide")
            else:
                print("[INFO] Le titre ne contient pas 'Facebook' ou 'Topoto', mais ce n'est pas forcement une erreur")

            # Vérifier le texte visible de la page (pas tout le code source)
            try:
                body_text = self.driver.find_element(By.TAG_NAME, "body").text.lower()

                # Chercher des messages d'erreur spécifiques dans le texte visible
                error_messages = [
                    "page not found",
                    "404",
                    "page introuvable",
                    "access denied",
                    "this content isn't available",
                    "this page isn't available",
                    "sorry, this page",
                    "content not found"
                ]

                for error_msg in error_messages:
                    if error_msg in body_text:
                        print(f"[ERREUR] Message d'erreur detecte dans le contenu: {error_msg}")
                        return False

                print("[OK] Aucun message d'erreur detecte dans le contenu visible")
            except Exception as e:
                print(f"[INFO] Impossible de verifier le contenu visible: {e}")

            # Vérifier l'URL pour des indicateurs d'erreur
            current_url = self.driver.current_url.lower()
            if "error" in current_url or "404" in current_url:
                print("[ERREUR] URL contient des indicateurs d'erreur")
                return False

            # Si on arrive ici, la page semble accessible
            print("[OK] Page Facebook accessible")
            return True
        except Exception as e:
            print(f"[INFO] Erreur lors de la verification d'accessibilite: {e}")
            # En cas d'erreur, considérer que la page est accessible si on est sur Facebook
            current_url = self.driver.current_url.lower()
            if "facebook.com" in current_url or "fb.com" in current_url:
                print("[OK] Page Facebook accessible (verification par URL)")
                return True
            return False

