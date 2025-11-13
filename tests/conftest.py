# conftest.py
import sys
from pathlib import Path

# Ajouter le répertoire racine du projet au PYTHONPATH
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless")  # décommente pour exécuter sans interface
    web_driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    web_driver.implicitly_wait(5)
    try:
        yield web_driver
    finally:
        web_driver.quit()
