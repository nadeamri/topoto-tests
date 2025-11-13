import pytest
import time
from selenium.webdriver.common.by import By
from src.pages.product_page import ProductPage
from src.pages.filtre_air_page import FiltreAirPage
from src.pages.cart_page import CartPage
from src.pages.order_page import OrderPage

# Données de commande pour le test
ORDER_DATA = {
    "nom": "nada",
    "prenom": "nada",
    "email": f"aamrinada489@gmail.com",  # J'ai retiré le point final (.) de l'email ici
    "telephone": "53317874"
}


@pytest.mark.usefixtures("driver")
class TestCommanderProduit:

    # -----------------------------------------------------------
    # TEST 1 : SCÉNARIO POSITIF (Commande Complète)
    # -----------------------------------------------------------
    # (J'ai ajouté le Test 1 pour avoir le fichier complet, vous devez l'avoir de votre côté)
    def test_commander_produit_complet(self, driver):
        """
        Scénario de bout en bout : Navigue, ajoute un produit, remplit le formulaire
        de commande et vérifie la confirmation.
        """

        # 1. INITIALISATION DES PAGES
        product_page = ProductPage(driver)
        filtre_air_page = FiltreAirPage(driver)
        cart_page = CartPage(driver)
        order_page = OrderPage(driver)

        # --- ÉTAPE 0: PRÉ-REQUIS ET NAVIGATION VERS LE PANIER ---
        print("\n--- Étape 0.1: Navigation vers le produit ---")
        product_page.open_product_page()
        product_page.click_filtre_air_link()
        assert filtre_air_page.is_page_loaded(), "Échec: La page Filtre à Air n'a pas été chargée."

        print("--- Étape 0.2: Ajout au panier ---")
        filtre_air_page.add_first_product_to_cart()

        print("--- Étape 0.3: Navigation vers la page Panier ---")
        filtre_air_page.check_and_go_to_cart()
        assert cart_page.is_product_in_cart(), "Échec: Le produit n'est pas dans le panier."

        # --- ÉTAPE 1: DÉMARRER LE PROCESSUS DE COMMANDE ---
        print("--- Étape 1: Clic sur 'Commander' ---")
        cart_page.click_commander_button()
        assert order_page.is_order_form_loaded(), "Échec: Le formulaire de commande n'a pas été chargé."

        # --- ÉTAPE 2: REMPLISSAGE DU FORMULAIRE ET SÉLECTION DU MODE DE LIVRAISON ---
        print("--- Étape 2: Remplissage du formulaire ---")
        order_page.fill_order_form(
            ORDER_DATA["nom"],
            ORDER_DATA["prenom"],
            ORDER_DATA["email"],
            ORDER_DATA["telephone"]
        )

        # --- ÉTAPE 3: CONFIRMATION DE LA COMMANDE ---
        print("--- Étape 3: Confirmation de la Commande ---")
        order_page.confirm_order()

        # --- ÉTAPE 4: VÉRIFICATION DE LA COMMANDE ---
        print("--- Étape 4: Vérification finale ---")

        assert order_page.is_order_confirmed(), "ÉCHEC: La page de confirmation de commande n'est pas apparue."

        reference = order_page.get_confirmation_reference()
        assert reference is not None and len(reference) > 0, "ÉCHEC: La référence de la commande est manquante ou vide."

    # -----------------------------------------------------------
    # TEST 2 : SCÉNARIO NÉGATIF (Téléphone manquant)
    # -----------------------------------------------------------
    def test_commander_produit_donnees_invalides(self, driver):
        """
        Scénario de test négatif : Tente de passer commande avec des données invalides
        (champ Téléphone laissé vide).
        """
        # 1. INITIALISATION DES PAGES
        product_page = ProductPage(driver)
        filtre_air_page = FiltreAirPage(driver)
        cart_page = CartPage(driver)
        order_page = OrderPage(driver)

        # --- ÉTAPE 0: PRÉ-REQUIS ET NAVIGATION VERS LE FORMULAIRE ---
        print("\n--- Étape 0: Préparation (Ajout au panier et accès au formulaire) ---")
        product_page.open_product_page()
        product_page.click_filtre_air_link()
        filtre_air_page.add_first_product_to_cart()
        filtre_air_page.check_and_go_to_cart()
        cart_page.click_commander_button()
        assert order_page.is_order_form_loaded(), "Échec: Le formulaire de commande n'a pas été chargé."

        # --- ÉTAPE 1: Remplissage INVALIDE ---
        print("--- Étape 1: Remplissage partiel du formulaire (Téléphone manquant) ---")
        order_page.fill_order_form(
            ORDER_DATA["nom"],
            ORDER_DATA["prenom"],
            ORDER_DATA["email"],
            ""  # Le champ du téléphone est laissé vide
        )

        # --- ÉTAPE 2: Tentative de Confirmation ---
        print("--- Étape 2: Tentative de Confirmation ---")
        order_page.confirm_order()

        # --- ÉTAPE 3: VÉRIFICATIONS NÉGATIVES ---
        print("--- Étape 3: Vérification de l'échec de la soumission ---")

        # 3.1. Vérifie qu'il n'y a PAS eu de redirection vers la page de confirmation
        assert not order_page.is_order_confirmed(
            timeout=5), "ÉCHEC NÉGATIF: La commande a été confirmée malgré l'absence du téléphone."

        # 3.2. Vérifie que le formulaire de commande est toujours affiché
        assert order_page.is_order_form_loaded(), "ÉCHEC: Nous n'avons pas pu valider que le formulaire est toujours là après l'erreur."

        print("✅ Test de données invalides réussi : La soumission a été bloquée.")

    # -----------------------------------------------------------
    # TEST 3 : SCÉNARIO NÉGATIF (Tous les champs vides)
    # -----------------------------------------------------------
    def test_commander_produit_champs_vides(self, driver):  # <-- ATTENTION à l'indentation ici
        """
        Scénario négatif : Tente de passer commande sans saisir aucune donnée.
        Vérifie que la soumission échoue.
        """
        # Initialisation des pages
        product_page = ProductPage(driver)
        filtre_air_page = FiltreAirPage(driver)
        cart_page = CartPage(driver)
        order_page = OrderPage(driver)

        # --- ÉTAPE 0: PRÉPARATION ---
        print("\n--- Étape 0: Préparation (Accès au formulaire de commande) ---")
        product_page.open_product_page()
        product_page.click_filtre_air_link()
        filtre_air_page.add_first_product_to_cart()
        filtre_air_page.check_and_go_to_cart()
        cart_page.click_commander_button()
        assert order_page.is_order_form_loaded(), "Échec: Le formulaire de commande n'a pas été chargé."

        # --- ÉTAPE 1: Remplissage VIDE ---
        print("--- Étape 1: Remplissage avec des chaînes vides ---")
        # Tous les champs sont remplis avec des chaînes vides
        order_page.fill_order_form(
            "",  # Nom
            "",  # Prénom
            "",  # Email
            ""  # Téléphone
        )

        # --- ÉTAPE 2: Tentative de Confirmation ---
        print("--- Étape 2: Tentative de Confirmation ---")
        order_page.confirm_order()

        # --- ÉTAPE 3: VÉRIFICATIONS NÉGATIVES ---
        print("--- Étape 3: Vérification de l'échec de la soumission ---")

        # 3.1. Vérifie qu'il n'y a PAS eu de redirection
        assert not order_page.is_order_confirmed(
            timeout=5), "ÉCHEC NÉGATIF: La commande a été confirmée avec des champs vides."

        # 3.2. Vérifie que le formulaire est toujours présent
        assert order_page.is_order_form_loaded(), "ÉCHEC: Nous ne sommes pas restés sur la page du formulaire après l'erreur."

        print("✅ Test 'champs vides' réussi : La soumission a été bloquée.")

    # -----------------------------------------------------------
    # TEST 4 : SCÉNARIO NÉGATIF (Formats Invalides)
    # -----------------------------------------------------------
    def test_commander_produit_formats_invalides(self, driver):  # <-- ATTENTION à l'indentation ici
        """
        Scénario négatif : Tente de passer commande avec un email et un téléphone au format invalide.
        Vérifie que la soumission échoue.
        """
        # Initialisation des pages
        product_page = ProductPage(driver)
        filtre_air_page = FiltreAirPage(driver)
        cart_page = CartPage(driver)
        order_page = OrderPage(driver)

        # --- ÉTAPE 0: PRÉPARATION ---
        print("\n--- Étape 0: Préparation (Accès au formulaire de commande) ---")
        product_page.open_product_page()
        product_page.click_filtre_air_link()
        filtre_air_page.add_first_product_to_cart()
        filtre_air_page.check_and_go_to_cart()
        cart_page.click_commander_button()
        assert order_page.is_order_form_loaded(), "Échec: Le formulaire de commande n'a pas été chargé."

        # --- ÉTAPE 1: Remplissage INVALIDE ---
        print("--- Étape 1: Remplissage avec des formats invalides ---")

        order_page.fill_order_form(
            ORDER_DATA["nom"],
            ORDER_DATA["prenom"],
            "cecinestpasunemail.com",  # Email invalide (manque le @)
            "ABCDE12345"  # Téléphone invalide (contient des lettres)
        )

        # --- ÉTAPE 2: Tentative de Confirmation ---
        print("--- ÉTAPE 2: Tentative de Confirmation ---")
        order_page.confirm_order()

        # --- ÉTAPE 3: VÉRIFICATIONS NÉGATIVES ---
        print("--- Étape 3: Vérification de l'échec de la soumission ---")

        # 3.1. Vérifie qu'il n'y a PAS eu de redirection
        assert not order_page.is_order_confirmed(
            timeout=5), "ÉCHEC NÉGATIF: La commande a été confirmée malgré les formats invalides."

        # 3.2. Vérifie que le formulaire est toujours présent
        assert order_page.is_order_form_loaded(), "ÉCHEC: Nous ne sommes pas restés sur la page du formulaire après l'erreur."

        print("✅ Test 'formats invalides' réussi : La soumission a été bloquée.")
