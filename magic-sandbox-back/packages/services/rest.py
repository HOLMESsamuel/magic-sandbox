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

@router.post("/deck")
async def scrap_deck(deck_input: DeckInput):
    try:
        web_scraper = WebScraper()
        print("web scraper initialized")
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

@router.post("/room/{roomId}/player/{playerId}/deck/reset")
async def reset(playerId: str, roomId: str):
    response = await game_service.reset(playerId, roomId)
    return response

@router.post("/room/{roomId}/player/{playerId}/deck/draw")
async def draw_card(playerId: str, roomId: str):
    response = await game_service.draw_card(playerId, roomId)
    return response

@router.post("/room/{roomId}/player/{playerId}/deck/shuffle")
async def shuffle_deck(playerId: str, roomId: str):
    response = await game_service.shuffle_deck(playerId, roomId)
    return response

@router.post("/room/{roomId}/player/{playerId}/score/{score}")
async def update_score(playerId: str, roomId: str, score: int):
    response = await game_service.update_score(playerId, roomId, score)
    return response

@router.post("/room/{roomId}/player/{playerId}/card/{cardId}/tap")
async def tap_card(playerId: str, roomId: str, cardId: str):
    response = await game_service.tap_card(playerId, roomId, cardId)
    return response

@router.post("/room/{roomId}/player/{playerId}/card/{cardId}/untap")
async def untap_card(playerId: str, roomId: str, cardId: str):
    response = await game_service.untap_card(playerId, roomId, cardId)
    return response

@router.post("/room/{roomId}/player/{playerId}/card/{cardId}/play")
async def play_card(playerId: str, roomId: str, cardId: str, position: dict):
    response = await game_service.play_card(playerId, roomId, cardId, position)
    return response

@router.post("/room/{roomId}/player/{playerId}/deck/card/{cardId}/hand")
async def move_card_from_deck_to_hand(playerId: str, roomId: str, cardId: str):
    response = await game_service.move_card_from_deck_to_hand(playerId, roomId, cardId)
    return response

@router.post("/room/{roomId}/player/{playerId}/board/card/{cardId}/hand/{targetPlayerId}")
async def move_card_from_board_to_hand(playerId: str, roomId: str, cardId: str, targetPlayerId: str):
    response = await game_service.move_card_from_board_to_hand(playerId, roomId, cardId, targetPlayerId)
    return response

@router.post("/room/{roomId}/player/{playerId}/hand/card/{cardId}/hand/{targetPlayerId}")
async def move_card_from_hand_to_hand(playerId: str, roomId: str, cardId: str, targetPlayerId: str):
    response = await game_service.move_card_from_hand_to_hand(playerId, roomId, cardId, targetPlayerId)
    return response

@router.post("/room/{roomId}/player/{playerId}/board/detap")
async def detap_all(playerId: str, roomId: str):
    response = await game_service.detap_all(playerId, roomId)
    return response

@router.post("/room/{roomId}/player/{playerId}/mulligan")
async def mulligan(playerId: str, roomId: str):
    response = await game_service.mulligan(playerId, roomId)
    return response