import pytest
from src.pages.home_page import HomePage
from src.pages.product_page import ProductPage
from src.pages.filtre_air_page import FiltreAirPage
from src.pages.cart_page import CartPage


def test_scenario_complet_navigation_achat(driver):
    """
    Scénario complet :
    1. Accès à la page d'accueil
    2. Navigation vers la page produits
    3. Navigation vers la sous-catégorie Filtre à Air
    4. Ajout d'un produit au panier
    5. Vérification de la modale de confirmation
    6. Navigation vers le panier
    7. Vérification de la présence du produit
    8. Nettoyage du panier
    """

    # 1. INITIALISATION DES PAGES
    home_page = HomePage(driver)
    product_page = ProductPage(driver)
    filtre_air_page = FiltreAirPage(driver)
    cart_page = CartPage(driver)

    # 2. ÉTAPE : Accès à la page d'accueil
    print("Étape 1: Accès à la page d'accueil...")
    home_page.open_home_page()

    # Capture l'URL de départ
    home_url = driver.current_url
    assert "topoto" in home_url.lower(), "Échec : La page d'accueil n'a pas été chargée correctement."
    print("✓ Page d'accueil chargée avec succès")

    # 3. ÉTAPE : Navigation vers la page produits
    print("Étape 2: Navigation vers la page produits...")
    product_page.open_product_page()

    # 🔴 CORRECTION APPLIQUÉE :
    # 1. On vérifie que l'URL a changé par rapport à la page d'accueil.
    # 2. On vérifie qu'un élément clé de la page Produits est chargé (méthode non montrée ici).
    #
    # Pour le moment, nous allons faire la vérification de changement d'URL :
    assert driver.current_url != home_url, "Échec : La page produits n'a pas été chargée (l'URL est restée inchangée)."
    print("✓ Page produits chargée avec succès")

    # 4. ÉTAPE : Navigation vers la sous-catégorie Filtre à Air
    print("Étape 3: Navigation vers la sous-catégorie 'Filtre à Air'...")
    product_page.click_filtre_air_link()
    assert filtre_air_page.is_page_loaded(), "Échec : La page 'Filtre à Air' n'a pas été chargée."
    print("✓ Page 'Filtre à Air' chargée avec succès")

    # 5. ÉTAPE : Ajout du premier produit au panier
    print("Étape 4: Ajout du premier produit au panier...")
    filtre_air_page.add_first_product_to_cart()
    print("✓ Produit ajouté au panier")

    # 6. ÉTAPE : Vérification de la modale et navigation vers le panier
    print("Étape 5: Vérification de la modale et navigation vers le panier...")
    filtre_air_page.check_and_go_to_cart()
    print("✓ Navigation vers le panier effectuée")

    # 7. ÉTAPE : Vérification de la présence du produit dans le panier
    print("Étape 6: Vérification de la présence du produit dans le panier...")
    assert cart_page.is_page_loaded(), "Échec : La page du panier n'a pas été chargée."
    assert cart_page.is_product_in_cart(), "Échec : Le produit n'est pas présent dans le panier."
    print("✓ Produit vérifié dans le panier")

    # 8. ÉTAPE : Nettoyage du panier
    print("Étape 7: Nettoyage du panier...")
    cart_page.remove_product_from_cart()
    assert cart_page.is_page_loaded(), "Échec : La page du panier n'est plus accessible après le retrait."
    print("✓ Panier nettoyé avec succès")

    print("\n" + "=" * 60)
    print("SUCCÈS : Scénario complet exécuté avec succès")
    print("=" * 60)

