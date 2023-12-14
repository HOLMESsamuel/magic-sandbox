from fastapi import APIRouter, Depends, HTTPException
from .web_scraper import WebScraper
import random
from pydantic import BaseModel, validator

from .game_service import GameService

class DeckInput(BaseModel):
    url: str

    @validator('url')
    def url_must_not_be_empty(cls, v):
        if not v:
            raise ValueError('URL must not be empty')
        return v

router = APIRouter()
game_service = GameService()

url = "https://archidekt.com/decks/6015452/commander_eldrazi"

@router.post("/deck")
async def scrap_deck(deck_input: DeckInput):
    try:
        web_scraper = WebScraper()
        deck = web_scraper.get_deck(deck_input.url)
        return deck
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while processing the request.")
    finally:
        web_scraper.close_driver()

@router.get("/")
def read_root():
    return {"Hello": "World"}

@router.get("/dice")
def throw_dice():
    return random.randint(1, 20)

@router.post("/room/{roomId}/player/{playerId}/deck/mill")
async def mill_deck(playerId: str, roomId: str):
    response = await game_service.mill_card(playerId, roomId)
    return response

@router.post("/room/{roomId}/player/{playerId}/deck/draw")
async def draw_card(playerId: str, roomId: str):
    response = await game_service.draw_card(playerId, roomId)
    return response