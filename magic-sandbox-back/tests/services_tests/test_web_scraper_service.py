import pytest
from src.services.web_scraper_service import WebScraperService
from src.scrapers import ArchidektWebScraper, TappedOutWebScraper, AetherhubWebScraper

@pytest.mark.parametrize("url, expected", [
    ("https://archidekt.com/decks/6953017/eldrazi_cascade", ArchidektWebScraper),
    ("https://tappedout.net/mtg-decks/saruman-millcaster/", TappedOutWebScraper),
    ("https://aetherhub.com/Deck/four-color-assassins", AetherhubWebScraper),
    ("http://example.com/invalid/deck", ValueError)
])
def test_get_scraper(url, expected):
    service = WebScraperService()
    if expected is ValueError:
        with pytest.raises(ValueError):
            service.get_scraper(url)
    else:
        scraper = service.get_scraper(url)
        assert isinstance(scraper, expected), f"Expected {expected} for URL '{url}'"