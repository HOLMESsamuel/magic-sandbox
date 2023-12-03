from fastapi import APIRouter
from .web_scraper import WebScraper

router = APIRouter()
web_scraper = WebScraper()

url = "https://archidekt.com/decks/6015452/commander_eldrazi"

@router.post("/deck")
async def scrap_deck(deck_url: str):
    return web_scraper.get_deck(deck_url)