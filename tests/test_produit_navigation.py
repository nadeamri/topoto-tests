from src.pages.product_page import ProductPage
from src.pages.filtre_air_page import FiltreAirPage
from src.pages.cart_page import CartPage

# Dans tests/test_produit_navigation.py
from src.pages.product_page import ProductPage
from src.pages.filtre_air_page import FiltreAirPage
from src.pages.cart_page import CartPage

# Dans tests/test_produit_navigation.py

# ... (les imports de ProductPage et FiltreAirPage) ...

# Dans tests/test_produit_navigation.py

# ... (imports)

def test_navigation_vers_filtre_air(driver):
    """
    Scénario Fonctionnel : Vérifie la navigation de la page produits
    vers la sous-catégorie 'Filtre à Air' via l'action de clic.
    """

    # 1. INITIALISATION DES PAGES
    product_page = ProductPage(driver)
    filtre_air_page = FiltreAirPage(driver)  # Assurez-vous que cette Page Object a une méthode d'assertion

    # 2. ÉTAPE D'ACTION : Aller à la page Produits
    product_page.open_product_page()

    # 3. ÉTAPE D'ACTION : Cliquer sur le lien "Filtre à Air"
    print("Navigation vers la sous-catégorie Filtre à Air par clic...")
    product_page.click_filtre_air_link()

    # 4. ÉTAPE DE VÉRIFICATION (CRUCIALE)
    # Assurez-vous que la page d'arrivée est la bonne.
    # Ceci suppose que vous avez défini un titre ou un élément unique sur FiltreAirPage.
    assert filtre_air_page.is_page_loaded(), "Échec : La page 'Filtre à Air' n'a pas été chargée ou le titre est incorrect."


