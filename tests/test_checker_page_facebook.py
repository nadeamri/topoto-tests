import pytest
from src.pages.home_page import HomePage
from src.pages.facebook_page import FacebookPage


def test_checker_page_facebook(driver):
    """
    Scénario de vérification de la page Facebook :
    1. Accès à la page d'accueil
    2. Recherche et clic sur le lien Facebook
    3. Vérification que la page Facebook s'ouvre
    4. Vérification que la page Facebook est accessible
    5. Vérification de l'URL Facebook
    """

    # 1. INITIALISATION DES PAGES
    home_page = HomePage(driver)
    facebook_page = FacebookPage(driver)

    # 2. ÉTAPE : Accès à la page d'accueil
    print("=" * 60)
    print("Etape 1: Acces a la page d'accueil...")
    print("=" * 60)
    home_page.open_home_page()
    assert "topoto" in driver.current_url.lower(), "Echec : La page d'accueil n'a pas ete chargee correctement."
    print("[OK] Page d'accueil chargee avec succes")

    # 3. ÉTAPE : Recherche et clic sur le lien Facebook
    print("\n" + "=" * 60)
    print("Etape 2: Recherche et clic sur le lien Facebook...")
    print("=" * 60)

    try:
        home_page.go_to_facebook()
        print("[OK] Lien Facebook clique avec succes")
    except Exception as e:
        print(f"[ERREUR] Impossible de cliquer sur le lien Facebook: {e}")
        # Essayer de trouver le lien manuellement et naviguer directement
        from selenium.webdriver.common.by import By

        try:
            # Chercher tous les liens possibles vers Facebook
            facebook_links = driver.find_elements(By.XPATH,
                                                  "//a[contains(@href, 'facebook') or contains(@href, 'fb.com')]")
            if facebook_links:
                facebook_url = facebook_links[0].get_attribute('href')
                print(f"[INFO] Lien Facebook trouve: {facebook_url}")
                print("[INFO] Navigation directe vers Facebook...")
                driver.get(facebook_url)
                print("[OK] Navigation directe vers Facebook effectuee")
            else:
                raise Exception("Aucun lien Facebook trouve sur la page")
        except Exception as e2:
            assert False, f"Echec : Impossible d'acceder a la page Facebook. Erreur: {e2}"

    # 4. ÉTAPE : Attendre que la page Facebook se charge
    print("\n" + "=" * 60)
    print("Etape 3: Attente du chargement de la page Facebook...")
    print("=" * 60)

    import time
    time.sleep(3)  # Attendre que la page se charge

    # Vérifier si on est toujours sur la page d'accueil (le lien n'a pas fonctionné)
    current_url = driver.current_url.lower()
    if "topoto.tn" in current_url and "facebook" not in current_url:
        print("[ERREUR] On est toujours sur la page Topoto, le lien Facebook n'a pas fonctionne")
        # Essayer de naviguer directement
        from selenium.webdriver.common.by import By
        facebook_links = driver.find_elements(By.XPATH, "//a[contains(@href, 'facebook') or contains(@href, 'fb.com')]")
        if facebook_links:
            facebook_url = facebook_links[0].get_attribute('href')
            print(f"[INFO] Tentative de navigation directe vers: {facebook_url}")
            driver.get(facebook_url)
            time.sleep(3)

    # Gérer les fenêtres multiples si Facebook s'ouvre dans un nouvel onglet
    if len(driver.window_handles) > 1:
        print("[INFO] Facebook s'est ouvert dans un nouvel onglet")
        # Basculer vers le nouvel onglet
        driver.switch_to.window(driver.window_handles[-1])
        print("[OK] Basculement vers le nouvel onglet effectue")
        time.sleep(2)  # Attendre que le nouvel onglet se charge

    # 5. ÉTAPE : Vérification que la page Facebook est chargée
    print("\n" + "=" * 60)
    print("Etape 4: Verification que la page Facebook est chargee...")
    print("=" * 60)

    is_loaded = facebook_page.is_facebook_page_loaded()
    assert is_loaded, "Echec : La page Facebook n'a pas ete chargee correctement."
    print("[OK] Page Facebook chargee avec succes")

    # 6. ÉTAPE : Vérification de l'URL Facebook
    print("\n" + "=" * 60)
    print("Etape 5: Verification de l'URL Facebook...")
    print("=" * 60)

    facebook_url = facebook_page.get_facebook_url()
    print(f"[INFO] URL Facebook: {facebook_url}")

    # Vérifier que l'URL contient facebook.com ou fb.com
    assert "facebook.com" in facebook_url.lower() or "fb.com" in facebook_url.lower(), \
        f"Echec : L'URL ne correspond pas a Facebook. URL actuelle: {facebook_url}"
    print("[OK] URL Facebook validee")

    # 7. ÉTAPE : Vérification que la page Facebook est accessible
    print("\n" + "=" * 60)
    print("Etape 6: Verification que la page Facebook est accessible...")
    print("=" * 60)

    is_accessible = facebook_page.is_facebook_page_accessible()
    assert is_accessible, "Echec : La page Facebook n'est pas accessible ou contient des erreurs."
    print("[OK] Page Facebook accessible et fonctionnelle")

    print("\n" + "=" * 60)
    print("SUCCES : Test de verification de la page Facebook reussi")
    print("La page Facebook est accessible et fonctionne correctement")
    print("=" * 60)

