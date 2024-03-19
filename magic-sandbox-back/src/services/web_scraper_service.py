from ..scrapers import Scraper
from ..scrapers import ArchidektWebScraper
from ..scrapers import TappedOutWebScraper
from ..scrapers import AetherhubWebScraper


class WebScraperService:
        
    def get_scraper(self, url: str) -> Scraper:
        if "archidekt" in url:
            return ArchidektWebScraper()
        elif "tappedout" in url:
            return TappedOutWebScraper()
        elif "aetherhub" in url:
            return AetherhubWebScraper()
        else:
            raise ValueError("The url must be from either archidekt, tapped out or aetherhub")



