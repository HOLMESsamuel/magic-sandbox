from src.scrapers.tapped_out_web_scraper import TappedOutWebScraper

def test_get_deck():
    scraper = TappedOutWebScraper()

    url = "https://tappedout.net/mtg-decks/17-05-20-Dfx-kalamax-the-stormsire/"

    deck = scraper.get_deck(url)
    scraper.close_driver()

    assert deck is not None
    assert len(deck.cards) == 100
    
    silundi_vision_with_flip = any(
        card.name == "Silundi Vision" and card.flip_image for card in deck.cards
    )

    assert silundi_vision_with_flip, "'Silundi vision' card with a flip image was not found in the deck."