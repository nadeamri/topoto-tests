import pytest
from selenium import webdriver
from src.pages.product_page import ProductPage  # adapte le chemin si nécessaire

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def test_product_page_elements(driver):
    product_page = ProductPage(driver)
    product_page.open_product_page()

    # Vérifie que les titres sont présents (en ignorant la casse)
    assert "NOS PRODUITS" in product_page.get_products_title().upper()
    assert "NOS CATÉGORIES" in product_page.get_categories_title().upper()

    # Vérifie que le produit VIDANGE est affiché
    assert product_page.is_vidange_displayed()


