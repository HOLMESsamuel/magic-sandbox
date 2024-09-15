from ..scrapers import Scraper
from ..scrapers import ArchidektWebScraper
from ..scrapers import TappedOutWebScraper
from ..scrapers import AetherhubWebScraper
from selenium import webdriver


class WebScraperService:
        
    def get_scraper(self, url: str, driver: webdriver.Chrome) -> Scraper:
        if "archidekt" in url:
            return ArchidektWebScraper(driver)
        elif "tappedout" in url:
            return TappedOutWebScraper(driver)
        elif "aetherhub" in url:
            return AetherhubWebScraper(driver)
        else:
            raise ValueError("The url must be from either archidekt, tapped out or aetherhub")



