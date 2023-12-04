from fastapi import APIRouter
from .web_scraper import WebScraper

router = APIRouter()

url = "https://archidekt.com/decks/6015452/commander_eldrazi"

@router.post("/deck")
async def scrap_deck(deck_url: str):
    web_scraper = WebScraper()
    deck = web_scraper.get_deck(deck_url)
    web_scraper.close_driver()
    return deck

@router.get("/")
def read_root():
    return {"Hello": "World"}