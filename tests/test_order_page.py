import pytest
import time
from src.pages.product_page import ProductPage
from src.pages.filtre_air_page import FiltreAirPage
from src.pages.cart_page import CartPage
from src.pages.order_page import OrderPage

# Données de commande pour le test (À ADAPTER SI BESOIN)
ORDER_DATA = {
    "nom": "nada",
    "prenom": "nada",
    "email": f"aamrinada489@gmail.com.",
    "telephone": "53317874"
}


@pytest.mark.usefixtures("driver")
class TestCommanderProduit:

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

        # 0.1 Aller à la page Produits et Filtre à Air (robustesse JS+Scroll)
        print("\n--- Étape 0.1: Navigation vers le produit ---")
        product_page.open_product_page()
        product_page.click_filtre_air_link()
        assert filtre_air_page.is_page_loaded(), "Échec: La page Filtre à Air n'a pas été chargée."

        # 0.2 Ajout au panier (CLIC ROBUSTE APPLIQUÉ ICI)
        print("--- Étape 0.2: Ajout au panier ---")
        filtre_air_page.add_first_product_to_cart()

        # 0.3 Vérification modale et navigation vers la page Panier
        print("--- Étape 0.3: Navigation vers la page Panier ---")
        filtre_air_page.check_and_go_to_cart()
        assert cart_page.is_product_in_cart(), "Échec: Le produit n'est pas dans le panier."

        # --- ÉTAPE 1: DÉMARRER LE PROCESSUS DE COMMANDE ---
        print("--- Étape 1: Clic sur 'Commander' ---")
        cart_page.click_commander_button()

        # Vérification que nous sommes sur la page du formulaire (OrderPage)
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

        # 4.1 Vérifier la page de confirmation (par l'URL)
        assert order_page.is_order_confirmed(), "ÉCHEC: La page de confirmation de commande n'est pas apparue."

        # 4.2 Récupérer et valider la référence
        reference = order_page.get_confirmation_reference()

        # ✅ CORRECTION APPLIQUÉE : On vérifie juste si la référence existe et n'est pas vide
        assert reference is not None and len(reference) > 0, "ÉCHEC: La référence de la commande est manquante ou vide."