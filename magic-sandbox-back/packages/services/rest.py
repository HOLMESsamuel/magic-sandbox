from fastapi import APIRouter, Body, Depends, HTTPException
from .web_scraper import WebScraper
import asyncio
from pydantic import BaseModel, validator

from .game_service import GameService

class DeckInput(BaseModel):
    url: str

    @validator('url')
    def url_must_not_be_empty(cls, v):
        if not v:
            raise ValueError('URL must not be empty')
        return v
    
class TokenData(BaseModel):
    text: str
    type: str

router = APIRouter()
game_service = GameService()

@router.post("/room/{roomId}/player/{playerId}/deck")
async def scrap_deck(playerId: str, roomId: str, deck_input: DeckInput):
    try:
        web_scraper = WebScraper()
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

@router.get("/")
def read_root():
    return {"Hello": "World"}

@router.get("/room/{roomId}/player/{playerId}/dice/{diceValue}")
async def throw_dice(playerId: str, roomId: str, diceValue: int):
    dice_result = await game_service.throw_dice(playerId, roomId, diceValue)
    return dice_result

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

@router.put("/room/{roomId}/player/{playerId}/card/{cardId}/flip")
async def flip_card(playerId: str, roomId: str, cardId: str):
    response = await game_service.flip_card(playerId, roomId, cardId)
    return response

@router.post("/room/{roomId}/player/{playerId}/token/{tokenId}/tap")
async def tap_token(playerId: str, roomId: str, tokenId: str):
    response = await game_service.tap_token(playerId, roomId, tokenId)
    return response

@router.post("/room/{roomId}/player/{playerId}/token/{tokenId}/untap")
async def untap_token(playerId: str, roomId: str, tokenId: str):
    response = await game_service.untap_token(playerId, roomId, tokenId)
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

@router.post("/room/{roomId}/player/{playerId}/hand/card/{cardId}/deck/{cardPosition}")
async def move_card_to_deck(playerId: str, roomId: str, cardId: str, cardPosition: int):
    response = await game_service.move_card_to_deck(playerId, roomId, cardId, cardPosition)
    return response

@router.post("/room/{roomId}/player/{playerId}/token")
async def create_token(playerId: str, roomId: str, token_data: TokenData = Body(...)):
    response = await game_service.create_token(playerId, roomId, token_data.text, token_data.type)
    return response

@router.delete("/room/{roomId}/player/{playerId}/token/{id}")
async def delete_token(playerId: str, roomId: str, id: str):
    response = await game_service.delete_token(playerId, roomId, id)
    return response

@router.put("/room/{roomId}/player/{playerId}/token/{id}")
async def modify_token(playerId: str, roomId: str, id: str, token_data: TokenData = Body(...)):
    response = await game_service.modify_token(playerId, roomId, id, token_data.text, token_data.type)
    return response
