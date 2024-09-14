from abc import ABC, abstractmethod

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.driver_cache import DriverCacheManager

class Scraper(ABC):

    driver = None

    def __init__(self):
        if not Scraper.driver:
            print("Initializing WebDriver for the first time")
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            Scraper.driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()), options=options
            )
        self.driver = Scraper.driver

    @abstractmethod
    async def get_deck(self, url: str):
        pass

    def close_driver(self):
        if Scraper.driver:
            Scraper.driver.quit()
            Scraper.driver = None
            print("WebDriver closed")