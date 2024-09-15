import pytest
from src.scrapers.aetherhub_web_scraper import AetherhubWebScraper

@pytest.mark.asyncio
async def test_get_deck_with_commander(webdriver_instance):
    scraper = AetherhubWebScraper(driver=webdriver_instance)

    url = "https://aetherhub.com/Deck/slivers-1034839"

    deck = await scraper.get_deck(url)

    commander = any(card.commander == True for card in deck.cards)

    assert deck is not None
    assert len(deck.cards) == 100
    assert commander

@pytest.mark.asyncio
async def test_get_deck_without_commander(webdriver_instance):
    scraper = AetherhubWebScraper(driver=webdriver_instance)

    url = "https://aetherhub.com/Deck/monored-1042912"

    deck = await scraper.get_deck(url)

    commander = any(card.commander == True for card in deck.cards)

    assert deck is not None
    assert len(deck.cards) == 75
    assert commander == False


    