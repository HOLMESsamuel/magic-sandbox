import pytest
from src.scrapers.tapped_out_web_scraper import TappedOutWebScraper

@pytest.mark.asyncio
async def test_get_deck_with_commander():
    scraper = TappedOutWebScraper()

    url = "https://tappedout.net/mtg-decks/17-05-20-Dfx-kalamax-the-stormsire/"

    deck = await scraper.get_deck(url)
    scraper.close_driver()

    assert deck is not None
    assert len(deck.cards) == 100
    
    silundi_vision_with_flip = any(
        card.name == "Silundi Vision" and card.flip_image for card in deck.cards
    )

    commander_exists = any(card.commander == True for card in deck.cards)

    assert silundi_vision_with_flip, "'Silundi vision' card with a flip image was not found in the deck."
    assert commander_exists

    commander = None
    for card in deck.cards:
        if card.commander:
            commander = card
            break

    assert "creature" in commander.types, "the type was not loaded correctly"

@pytest.mark.asyncio
async def test_get_deck_without_commander():
    scraper = TappedOutWebScraper()

    url = "https://tappedout.net/mtg-decks/mono-green-toxic-2/"

    deck = await scraper.get_deck(url)
    scraper.close_driver()

    assert deck is not None
    assert len(deck.cards) == 60
    

    commander_exists = any(card.commander == True for card in deck.cards)

    assert commander_exists == False