from src.scrapers.aetherhub_web_scraper import AetherhubWebScraper

def test_get_deck():
    scraper = AetherhubWebScraper()

    url = "https://aetherhub.com/Deck/slivers-1034839"

    deck = scraper.get_deck(url)
    scraper.close_driver()

    assert deck is not None
    assert len(deck.cards) == 100