from selenium import webdriver

def create_driver(browser="chrome"):
    """Crée et retourne un driver Selenium selon le navigateur choisi."""
    if browser == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        # options.add_argument("--headless")  # Décommente pour exécuter sans interface
        driver = webdriver.Chrome(options=options)

    elif browser == "firefox":
        driver = webdriver.Firefox()

    else:
        raise ValueError(f"Navigateur non supporté: {browser}")

    return driver
