from ..scrapers import Scraper
from ..scrapers import ArchidektWebScraper
from ..scrapers import TappedOutWebScraper


class WebScraperService:
        
    def get_scraper(self, url: str) -> Scraper:
        if "archidekt" in url:
            return ArchidektWebScraper()
        elif "tappedout" in url:
            return TappedOutWebScraper()
        else:
            raise ValueError("The url must be from either archidekt or tapped out")



