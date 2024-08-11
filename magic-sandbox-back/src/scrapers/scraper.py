from abc import ABC, abstractmethod

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.driver_cache import DriverCacheManager

class Scraper(ABC):

    def __init__(self):
        print("initializing web scraper")
        # Set up the Selenium WebDriver
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager(cache_manager=DriverCacheManager(valid_range=0)).install()), options=options)

    @abstractmethod
    def get_deck(self, url: str):
        pass

    def close_driver(self):
        self.driver.quit()