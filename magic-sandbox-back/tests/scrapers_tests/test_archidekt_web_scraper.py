import pytest
from src.scrapers.archidekt_web_scraper import ArchidektWebScraper

@pytest.mark.asyncio
async def test_archidekt_web_scraper_with_commander(webdriver_instance):
    scraper = ArchidektWebScraper(driver=webdriver_instance)

    url = "https://archidekt.com/decks/6953017/eldrazi_cascade"

    deck = await scraper.get_deck(url)

    assert deck is not None
    assert len(deck.cards) == 100
    
    treasure_map_with_flip = any(
        card.name == "Treasure Map // Treasure Cove" and card.flip_image for card in deck.cards
    )

    commander_exists = any(card.commander == True for card in deck.cards)

    assert treasure_map_with_flip, "'Treasure Map' card with a flip image was not found in the deck."
    assert commander_exists, "No commander was found"

    commander = None
    for card in deck.cards:
        if card.commander:
            commander = card
            break

    assert "Creature" in commander.types, "the type was not loaded correctly"

@pytest.mark.asyncio
async def test_archidekt_web_scraper_without_commander(webdriver_instance):
    scraper = ArchidektWebScraper(driver=webdriver_instance)

    url = "https://archidekt.com/decks/7193440/eldrazi_tribal"

    deck = await scraper.get_deck(url)

    assert deck is not None
    assert len(deck.cards) == 100

    commander = any(card.commander == True for card in deck.cards)

    assert commander == False, "A commander was found"