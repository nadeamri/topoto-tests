from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By


class CheckoutPage:
    """Page Object pour la page de commande/checkout"""

    # --- SÉLECTEURS ---
    PAGE_TITLE = (By.XPATH,
                  "//*[contains(translate(., 'abcdefghijklmnopqrstuvwxyzàâéèêëîïôœùûüÿç', 'ABCDEFGHIJKLMNOPQRSTUVWXYZÀÂÉÈÊËÎÏÔŒÙÛÜŸÇ'), 'COMMANDE') or contains(translate(., 'abcdefghijklmnopqrstuvwxyzàâéèêëîïôœùûüÿç', 'ABCDEFGHIJKLMNOPQRSTUVWXYZÀÂÉÈÊËÎÏÔŒÙÛÜŸÇ'), 'CHECKOUT')]")

    # Bouton pour passer commande depuis le panier
    COMMANDER_BUTTON = (By.XPATH,
                        "//button[contains(translate(., 'commander', 'COMMANDER'), 'COMMANDER') or contains(@class, 'btn-primary') or contains(@class, 'btn-success')]")

    # Champs du formulaire de commande
    NOM_INPUT = (By.NAME, "nom")
    PRENOM_INPUT = (By.NAME, "prenom")
    EMAIL_INPUT = (By.NAME, "email")
    TELEPHONE_INPUT = (By.NAME, "telephone")
    DATE_INPUT = (By.NAME, "date")

    # Bouton de validation de la commande
    VALIDER_COMMANDE_BUTTON = (By.XPATH,
                               "//button[@type='submit' and (contains(translate(., 'valider', 'VALIDER'), 'VALIDER') or contains(translate(., 'confirmer', 'CONFIRMER'), 'CONFIRMER'))]")

    # Message de confirmation de commande
    CONFIRMATION_MESSAGE = (By.XPATH,
                            "//*[contains(translate(., 'abcdefghijklmnopqrstuvwxyzàâéèêëîïôœùûüÿç', 'ABCDEFGHIJKLMNOPQRSTUVWXYZÀÂÉÈÊËÎÏÔŒÙÛÜŸÇ'), 'COMMANDE') and contains(translate(., 'abcdefghijklmnopqrstuvwxyzàâéèêëîïôœùûüÿç', 'ABCDEFGHIJKLMNOPQRSTUVWXYZÀÂÉÈÊËÎÏÔŒÙÛÜŸÇ'), 'CONFIRM')]")

    # Messages d'erreur de validation
    ERROR_MESSAGES = (By.XPATH,
                      "//*[contains(@class, 'error') or contains(@class, 'invalid') or contains(@class, 'alert-danger') or contains(@class, 'text-danger')]")
    FIELD_ERROR = (By.XPATH,
                   ".//following-sibling::*[contains(@class, 'error') or contains(@class, 'invalid-feedback')]")
    VALIDATION_ERROR = (By.XPATH,
                        "//div[contains(@class, 'alert') and (contains(translate(., 'erreur', 'ERREUR'), 'ERREUR') or contains(translate(., 'invalid', 'INVALID'), 'INVALID') or contains(translate(., 'requis', 'REQUIS'), 'REQUIS'))]")

    def __init__(self, driver):
        self.driver = driver

    def is_page_loaded(self, timeout=15):
        """Vérifie que la page de commande est chargée."""
        print(f"Vérification du chargement de la page de commande (attente max {timeout}s)...")
        try:
            # Vérifier soit le titre, soit la présence d'un formulaire
            try:
                WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located(self.PAGE_TITLE)
                )
                return True
            except TimeoutException:
                # Essayer avec le champ email
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located(self.EMAIL_INPUT)
                )
                return True
        except TimeoutException:
            # Vérifier aussi l'URL
            current_url = self.driver.current_url.lower()
            if "checkout" in current_url or "commande" in current_url or "order" in current_url:
                return True
            return False

    def click_commander_button(self, timeout=10):
        """Clique sur le bouton 'Commander' depuis le panier."""
        print("Clic sur le bouton 'Commander'...")
        try:
            button = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(self.COMMANDER_BUTTON)
            )
            button.click()
            print("[OK] Bouton 'Commander' clique avec succes")
        except TimeoutException:
            # Essayer avec JavaScript si le clic normal échoue
            print("Tentative de clic JavaScript...")
            button = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(self.COMMANDER_BUTTON)
            )
            self.driver.execute_script("arguments[0].click();", button)
            print("[OK] Bouton 'Commander' clique via JavaScript")

    def fill_checkout_form(self, nom="Test", prenom="User", email="test@example.com",
                           telephone="12345678", date="2025-11-12", timeout=10):
        """Remplit le formulaire de commande."""
        print("Remplissage du formulaire de commande...")

        try:
            # Remplir les champs si ils existent
            fields = {
                self.NOM_INPUT: nom,
                self.PRENOM_INPUT: prenom,
                self.EMAIL_INPUT: email,
                self.TELEPHONE_INPUT: telephone,
                self.DATE_INPUT: date,
            }
            for locator, value in fields.items():
                try:
                    element = WebDriverWait(self.driver, 3).until(
                        EC.presence_of_element_located(locator)
                    )
                    element.clear()
                    element.send_keys(value)
                    print(f"[OK] Champ {locator[1]} rempli")
                except TimeoutException:
                    # Le champ n'existe peut-être pas, continuer
                    continue

            print("[OK] Formulaire rempli avec succes")
        except Exception as e:
            print(f"Erreur lors du remplissage du formulaire: {e}")
            raise

    def submit_order(self, timeout=10):
        """Soumet la commande."""
        print("Soumission de la commande...")
        try:
            button = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(self.VALIDER_COMMANDE_BUTTON)
            )

            # Vérifier si le bouton est désactivé
            is_disabled = self.driver.execute_script(
                "return arguments[0].disabled || arguments[0].hasAttribute('disabled');", button
            )

            if is_disabled:
                print("[INFO] Le bouton est desactive (probablement a cause de la validation HTML5)")
                print("[INFO] Tentative de forcer le clic via JavaScript...")
                self.driver.execute_script("arguments[0].click();", button)
                print("[OK] Clic force via JavaScript")
            else:
                try:
                    button.click()
                    print("[OK] Commande soumise")
                except Exception as e:
                    # Si le clic normal échoue, essayer avec JavaScript
                    print(f"[INFO] Clic normal echoue: {e}")
                    print("[INFO] Tentative de clic via JavaScript...")
                    self.driver.execute_script("arguments[0].click();", button)
                    print("[OK] Commande soumise via JavaScript")
        except TimeoutException:
            raise Exception("Le bouton de validation n'a pas ete trouve")
        except Exception as e:
            print(f"[INFO] Erreur lors de la soumission: {e}")
            # Essayer quand même avec JavaScript
            try:
                button = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located(self.VALIDER_COMMANDE_BUTTON)
                )
                self.driver.execute_script("arguments[0].click();", button)
                print("[OK] Commande soumise via JavaScript (fallback)")
            except:
                raise

    def is_order_confirmed(self, timeout=10):
        """Vérifie si la commande a été confirmée."""
        print("Verification de la confirmation de commande...")
        try:
            # Attendre un peu pour que la page se charge
            import time
            time.sleep(2)

            # Vérifier d'abord les messages de confirmation (même si l'URL ne change pas)
            try:
                WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located(self.CONFIRMATION_MESSAGE)
                )
                print("[INFO] Message de confirmation trouve")
                return True
            except TimeoutException:
                pass

            # Vérifier l'URL
            current_url = self.driver.current_url.lower()
            print(f"[INFO] URL actuelle: {current_url}")

            # Vérifier l'URL pour des mots-clés de succès
            if "confirmation" in current_url or "success" in current_url or "merci" in current_url or "thank" in current_url:
                print("[INFO] URL indique une confirmation")
                return True

            # Vérifier si on est toujours sur /order/new mais avec un message de succès
            # Chercher des messages de succès dans la page
            success_indicators = [
                "//*[contains(translate(., 'abcdefghijklmnopqrstuvwxyzàâéèêëîïôœùûüÿç', 'ABCDEFGHIJKLMNOPQRSTUVWXYZÀÂÉÈÊËÎÏÔŒÙÛÜŸÇ'), 'SUCCES')]",
                "//*[contains(translate(., 'abcdefghijklmnopqrstuvwxyzàâéèêëîïôœùûüÿç', 'ABCDEFGHIJKLMNOPQRSTUVWXYZÀÂÉÈÊËÎÏÔŒÙÛÜŸÇ'), 'MERCI')]",
                "//*[contains(translate(., 'abcdefghijklmnopqrstuvwxyzàâéèêëîïôœùûüÿç', 'ABCDEFGHIJKLMNOPQRSTUVWXYZÀÂÉÈÊËÎÏÔŒÙÛÜŸÇ'), 'COMMANDE ENVOYEE')]",
                "//*[contains(translate(., 'abcdefghijklmnopqrstuvwxyzàâéèêëîïôœùûüÿç', 'ABCDEFGHIJKLMNOPQRSTUVWXYZÀÂÉÈÊËÎÏÔŒÙÛÜŸÇ'), 'COMMANDE RECUE')]"
            ]

            for indicator in success_indicators:
                try:
                    elements = self.driver.find_elements(By.XPATH, indicator)
                    if elements:
                        print(f"[INFO] Message de succes trouve sur la page")
                        return True
                except:
                    continue

            # Si on est toujours sur /order/new, vérifier si le formulaire a disparu
            # (signe que la commande a été traitée)
            if "order/new" in current_url:
                try:
                    # Si le formulaire n'existe plus, c'est peut-être confirmé
                    form_exists = len(self.driver.find_elements(*self.EMAIL_INPUT)) > 0
                    if not form_exists:
                        print("[INFO] Le formulaire a disparu - commande peut-etre confirmee")
                        # Vérifier s'il y a un message de confirmation
                        page_text = self.driver.find_element(By.TAG_NAME, "body").text.lower()
                        if any(word in page_text for word in ["succes", "merci", "confirme", "envoye", "recu"]):
                            print("[INFO] Message de confirmation trouve dans le texte de la page")
                            return True
                except:
                    pass

            # Si on est toujours sur la page de commande avec le formulaire, ce n'est PAS confirmé
            if "checkout" in current_url or "commande" in current_url or "order/new" in current_url:
                print("[INFO] On est toujours sur la page de commande - commande NON confirmee")
                return False

            # Si aucune indication de confirmation, retourner False
            print("[INFO] Aucune indication de confirmation trouvee")
            return False
        except Exception as e:
            print(f"[INFO] Erreur lors de la verification: {e}")
            return False

    def is_submit_button_disabled(self, timeout=5):
        """Vérifie si le bouton de soumission est désactivé."""
        try:
            button = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(self.VALIDER_COMMANDE_BUTTON)
            )
            is_disabled = self.driver.execute_script(
                "return arguments[0].disabled || arguments[0].hasAttribute('disabled') || !arguments[0].checkValidity();",
                button
            )
            return is_disabled
        except:
            return False

    def has_validation_errors(self, timeout=5):
        """Vérifie s'il y a des erreurs de validation affichées."""
        print("Verification de la presence d'erreurs de validation...")
        try:
            # Vérifier d'abord si le bouton est désactivé (signe de validation HTML5)
            if self.is_submit_button_disabled():
                print("[OK] Le bouton de soumission est desactive (validation HTML5 active)")
                return True

            # Attendre un peu pour que les erreurs apparaissent
            import time
            time.sleep(1)

            # Chercher des messages d'erreur
            errors = self.driver.find_elements(*self.ERROR_MESSAGES)
            validation_errors = self.driver.find_elements(*self.VALIDATION_ERROR)

            # Vérifier aussi les attributs HTML5 de validation
            form_fields = [
                self.NOM_INPUT, self.PRENOM_INPUT, self.EMAIL_INPUT,
                self.TELEPHONE_INPUT, self.DATE_INPUT
            ]

            for field_locator in form_fields:
                try:
                    field = self.driver.find_element(*field_locator)
                    # Vérifier si le champ a l'attribut :invalid (HTML5)
                    is_invalid = self.driver.execute_script(
                        "return arguments[0].validity.valid === false;", field
                    )
                    if is_invalid:
                        print(f"[ERREUR] Champ {field_locator[1]} invalide")
                        return True
                except:
                    continue

            if errors or validation_errors:
                print(f"[ERREUR] {len(errors) + len(validation_errors)} erreur(s) de validation detectee(s)")
                return True

            # Vérifier si on est toujours sur la page de commande (pas de redirection)
            current_url = self.driver.current_url.lower()
            if "checkout" in current_url or "commande" in current_url or "order" in current_url:
                # Si on est toujours sur la page de commande après soumission, il y a probablement une erreur
                # Mais on ne peut pas être sûr, donc on retourne False par défaut
                pass

            return False
        except Exception as e:
            print(f"Erreur lors de la verification des erreurs: {e}")
            return False

    def get_validation_errors(self, timeout=5):
        """Récupère tous les messages d'erreur de validation."""
        errors = []
        try:
            import time
            time.sleep(1)

            # Chercher les messages d'erreur généraux
            error_elements = self.driver.find_elements(*self.ERROR_MESSAGES)
            validation_elements = self.driver.find_elements(*self.VALIDATION_ERROR)

            for elem in error_elements + validation_elements:
                if elem.text.strip():
                    errors.append(elem.text.strip())

            # Chercher les erreurs de champs spécifiques
            form_fields = {
                self.NOM_INPUT: "nom",
                self.PRENOM_INPUT: "prenom",
                self.EMAIL_INPUT: "email",
                self.TELEPHONE_INPUT: "telephone",
                self.DATE_INPUT: "date"
            }

            for field_locator, field_name in form_fields.items():
                try:
                    field = self.driver.find_element(*field_locator)
                    # Vérifier l'attribut HTML5 validity
                    is_invalid = self.driver.execute_script(
                        "return arguments[0].validity.valid === false;", field
                    )
                    if is_invalid:
                        validation_message = self.driver.execute_script(
                            "return arguments[0].validationMessage;", field
                        )
                        if validation_message:
                            errors.append(f"{field_name}: {validation_message}")
                except:
                    continue

            return errors
        except Exception as e:
            print(f"Erreur lors de la recuperation des erreurs: {e}")
            return errors

