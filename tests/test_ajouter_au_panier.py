# Dans tests/test_produit_navigation.py (ou un nouveau fichier)

import pytest
# Assurez-vous d'importer toutes les pages :
from src.pages.product_page import ProductPage
from src.pages.filtre_air_page import FiltreAirPage
from src.pages.cart_page import CartPage  # NOUVEL IMPORT


# Utilisez cette fonction si elle est dans le même fichier que le test précédent
def test_ajouter_produit_depuis_filtre_air(driver):
    """
    Scénario : Navigue vers la sous-catégorie Filtre à Air,
    ajoute le premier produit au panier et vérifie l'ajout.
    """
    # 1. INITIALISATION
    product_page = ProductPage(driver)
    filtre_air_page = FiltreAirPage(driver)
    cart_page = CartPage(driver)  # NOUVELLE PAGE OBJECT

    # 2. ÉTAPE D'ACTION : Navigation vers Filtre à Air (réutilisation du code qui marche)
    product_page.open_product_page()
    product_page.click_filtre_air_link()
    assert filtre_air_page.is_page_loaded(), "Prérequis échoué: La page Filtre à Air n'a pas été chargée."

    # 3. ÉTAPE D'ACTION : Ajout au panier
    filtre_air_page.add_first_product_to_cart()

    # 4. ÉTAPE D'ACTION : Vérification modale et navigation vers le panier
    filtre_air_page.check_and_go_to_cart()

    # 5. ÉTAPE DE VÉRIFICATION : Le produit est dans le panier
    assert cart_page.is_product_in_cart(), "Échec : Le produit n'est pas présent ou visible dans le panier."

    print("Succès : Le produit a été ajouté au panier et la vérification est réussie.")
    # 6. ÉTAPE DE NETTOYAGE (Important pour la réutilisabilité du test)
    cart_page.remove_product_from_cart()

    # Vérification finale optionnelle : le panier est vide
    assert cart_page.is_page_loaded()  # Le titre 'Votre Panier' est toujours là
    # Vous pouvez aussi vérifier que le message 'Votre panier est vide.' est présent si vous voulez

    print("Nettoyage effectué. Test terminé.")