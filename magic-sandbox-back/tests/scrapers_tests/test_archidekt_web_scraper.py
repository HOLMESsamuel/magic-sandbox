from src.scrapers.archidekt_web_scraper import ArchidektWebScraper

def test_archidekt_web_scraper_with_commander():
    scraper = ArchidektWebScraper()

    url = "https://archidekt.com/decks/6953017/eldrazi_cascade"

    deck = scraper.get_deck(url)

    scraper.close_driver()

    assert deck is not None
    assert len(deck.cards) == 100
    
    treasure_map_with_flip = any(
        card.name == "Treasure Map // Treasure Cove" and card.flip_image for card in deck.cards
    )

    commander = any(card.commander == True for card in deck.cards)

    assert treasure_map_with_flip, "'Treasure Map' card with a flip image was not found in the deck."
    assert commander, "No commander was found"


def test_archidekt_web_scraper_without_commander():
    scraper = ArchidektWebScraper()

    url = "https://archidekt.com/decks/7193440/eldrazi_tribal"

    deck = scraper.get_deck(url)

    scraper.close_driver()

    assert deck is not None
    assert len(deck.cards) == 100

    commander = any(card.commander == True for card in deck.cards)

    assert commander == False, "A commander was found"