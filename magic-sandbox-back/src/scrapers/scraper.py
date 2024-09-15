from abc import ABC, abstractmethod
from selenium import webdriver

class Scraper(ABC):

    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver

    @abstractmethod
    async def get_deck(self, url: str):
        pass