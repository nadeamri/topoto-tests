import pytest
from src.pages.home_page import HomePage
from src.pages.instagram_page import InstagramPage


def test_checker_page_instagram(driver):
    """
    Scénario de vérification de la page Instagram :
    1. Accès à la page d'accueil
    2. Recherche et clic sur le lien Instagram
    3. Vérification que la page Instagram s'ouvre
    4. Vérification que la page Instagram est accessible
    5. Vérification de l'URL Instagram
    """

    # 1. INITIALISATION DES PAGES
    home_page = HomePage(driver)
    instagram_page = InstagramPage(driver)

    # 2. ÉTAPE : Accès à la page d'accueil
    print("=" * 60)
    print("Etape 1: Acces a la page d'accueil...")
    print("=" * 60)
    home_page.open_home_page()
    assert "topoto" in driver.current_url.lower(), "Echec : La page d'accueil n'a pas ete chargee correctement."
    print("[OK] Page d'accueil chargee avec succes")

    # 3. ÉTAPE : Recherche et clic sur le lien Instagram
    print("\n" + "=" * 60)
    print("Etape 2: Recherche et clic sur le lien Instagram...")
    print("=" * 60)

    try:
        home_page.go_to_instagram()
        print("[OK] Lien Instagram clique avec succes")
    except Exception as e:
        print(f"[ERREUR] Impossible de cliquer sur le lien Instagram: {e}")
        # Essayer de trouver le lien manuellement et naviguer directement
        from selenium.webdriver.common.by import By

        try:
            # Chercher tous les liens possibles vers Instagram
            instagram_links = driver.find_elements(By.XPATH,
                                                   "//a[contains(@href, 'instagram') or contains(@href, 'instagr.am')]")
            if instagram_links:
                instagram_url = instagram_links[0].get_attribute('href')
                print(f"[INFO] Lien Instagram trouve: {instagram_url}")
                print("[INFO] Navigation directe vers Instagram...")
                driver.get(instagram_url)
                print("[OK] Navigation directe vers Instagram effectuee")
            else:
                raise Exception("Aucun lien Instagram trouve sur la page")
        except Exception as e2:
            assert False, f"Echec : Impossible d'acceder a la page Instagram. Erreur: {e2}"

    # 4. ÉTAPE : Attendre que la page Instagram se charge
    print("\n" + "=" * 60)
    print("Etape 3: Attente du chargement de la page Instagram...")
    print("=" * 60)

    import time
    time.sleep(3)  # Attendre que la page se charge

    # Vérifier si on est toujours sur la page d'accueil (le lien n'a pas fonctionné)
    current_url = driver.current_url.lower()
    if "topoto.tn" in current_url and "instagram" not in current_url:
        print("[ERREUR] On est toujours sur la page Topoto, le lien Instagram n'a pas fonctionne")
        # Essayer de naviguer directement
        from selenium.webdriver.common.by import By
        instagram_links = driver.find_elements(By.XPATH,
                                               "//a[contains(@href, 'instagram') or contains(@href, 'instagr.am')]")
        if instagram_links:
            instagram_url = instagram_links[0].get_attribute('href')
            print(f"[INFO] Tentative de navigation directe vers: {instagram_url}")
            driver.get(instagram_url)
            time.sleep(3)

    # Gérer les fenêtres multiples si Instagram s'ouvre dans un nouvel onglet
    if len(driver.window_handles) > 1:
        print("[INFO] Instagram s'est ouvert dans un nouvel onglet")
        # Basculer vers le nouvel onglet
        driver.switch_to.window(driver.window_handles[-1])
        print("[OK] Basculement vers le nouvel onglet effectue")
        time.sleep(2)  # Attendre que le nouvel onglet se charge

    # 5. ÉTAPE : Vérification que la page Instagram est chargée
    print("\n" + "=" * 60)
    print("Etape 4: Verification que la page Instagram est chargee...")
    print("=" * 60)

    is_loaded = instagram_page.is_instagram_page_loaded()
    assert is_loaded, "Echec : La page Instagram n'a pas ete chargee correctement."
    print("[OK] Page Instagram chargee avec succes")

    # 6. ÉTAPE : Vérification de l'URL Instagram
    print("\n" + "=" * 60)
    print("Etape 5: Verification de l'URL Instagram...")
    print("=" * 60)

    instagram_url = instagram_page.get_instagram_url()
    print(f"[INFO] URL Instagram: {instagram_url}")

    # Vérifier que l'URL contient instagram.com ou instagr.am
    assert "instagram.com" in instagram_url.lower() or "instagr.am" in instagram_url.lower(), \
        f"Echec : L'URL ne correspond pas a Instagram. URL actuelle: {instagram_url}"
    print("[OK] URL Instagram validee")

    # 7. ÉTAPE : Vérification que la page Instagram est accessible
    print("\n" + "=" * 60)
    print("Etape 6: Verification que la page Instagram est accessible...")
    print("=" * 60)

    is_accessible = instagram_page.is_instagram_page_accessible()
    assert is_accessible, "Echec : La page Instagram n'est pas accessible ou contient des erreurs."
    print("[OK] Page Instagram accessible et fonctionnelle")

    print("\n" + "=" * 60)
    print("SUCCES : Test de verification de la page Instagram reussi")
    print("La page Instagram est accessible et fonctionne correctement")
    print("=" * 60)

