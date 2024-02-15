from fastapi import APIRouter, Body, HTTPException
from ..services import WebScraperService
from pydantic import BaseModel, validator
from ..services import GameService

router = APIRouter()
game_service = GameService()
web_scraper_service = WebScraperService()

class DeckInput(BaseModel):
    url: str

    @validator('url')
    def url_must_not_be_empty(cls, v):
        if not v:
            raise ValueError('URL must not be empty')
        return v
    
@router.post("/room/{roomId}/player/{playerId}/deck")
async def scrap_deck(playerId: str, roomId: str, deck_input: DeckInput):
    try:
        web_scraper = web_scraper_service.get_scraper(deck_input.url)
        print("web scraper initialized")
        #multithread does not seem to work on container, or the ram is not sufficient
        #deck = await asyncio.to_thread(web_scraper.get_deck, deck_input.url)
        deck = web_scraper.get_deck(deck_input.url)
        response = await game_service.add_deck(playerId, roomId, deck)
        return response
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while processing the request.")
    finally:
        web_scraper.close_driver()

@router.put("/room/{roomId}/player/{playerId}/deck/mill")
async def mill_deck(playerId: str, roomId: str):
    response = await game_service.mill_card(playerId, roomId)
    return response

@router.put("/room/{roomId}/player/{playerId}/deck/reset")
async def reset(playerId: str, roomId: str):
    response = await game_service.reset(playerId, roomId)
    return response

@router.put("/room/{roomId}/player/{playerId}/deck/draw")
async def draw_card(playerId: str, roomId: str):
    response = await game_service.draw_card(playerId, roomId)
    return response

@router.put("/room/{roomId}/player/{playerId}/deck/shuffle")
async def shuffle_deck(playerId: str, roomId: str):
    response = await game_service.shuffle_deck(playerId, roomId)
    return response

@router.put("/room/{roomId}/player/{playerId}/hand/card/{cardId}/deck/{cardPosition}")
async def move_card_to_deck(playerId: str, roomId: str, cardId: str, cardPosition: int):
    response = await game_service.move_card_to_deck(playerId, roomId, cardId, cardPosition)
    return response