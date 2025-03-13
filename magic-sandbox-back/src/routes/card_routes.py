from typing import List
from fastapi import APIRouter, Body
from pydantic import BaseModel

from ..services.game_service import GameService

router = APIRouter()
game_service = GameService()

class CardIds(BaseModel):
    cardIds: List[str]

class Counter(BaseModel):
    counter: int

@router.patch("/room/{roomId}/player/{playerId}/card/tap")
async def tap_cards(playerId: str, roomId: str, body: CardIds = Body(...)):
    response = await game_service.tap_cards(playerId, roomId, body.cardIds)
    return response

@router.patch("/room/{roomId}/player/{playerId}/card/untap")
async def untap_cards(playerId: str, roomId: str, body: CardIds = Body(...)):
    response = await game_service.untap_cards(playerId, roomId, body.cardIds)
    return response

@router.patch("/room/{roomId}/player/{playerId}/card/scrap")
async def scrap_cards(playerId: str, roomId: str, body: CardIds = Body(...)):
    response = await game_service.scrap_cards(playerId, roomId, body.cardIds)
    return response

@router.patch("/room/{roomId}/player/{playerId}/card/flip")
async def flip_cards(playerId: str, roomId: str, body: CardIds = Body(...)):
    response = await game_service.flip_cards(playerId, roomId, body.cardIds)
    return response

@router.patch("/room/{roomId}/player/{playerId}/card/{cardId}/counter")
async def flip_cards(playerId: str, roomId: str, cardId:str, body: Counter = Body(...)):
    response = await game_service.update_card_counter(playerId, roomId, cardId, body.counter)
    return response

@router.put("/room/{roomId}/player/{playerId}/card/{cardId}/play")
async def play_card(playerId: str, roomId: str, cardId: str, position: dict):
    response = await game_service.play_card(playerId, roomId, cardId, position)
    return response

@router.put("/room/{roomId}/player/{playerId}/card/{cardId}/copy")
async def copy_card(playerId: str, roomId: str, cardId: str):
    response = await game_service.copy_card(playerId, roomId, cardId)
    return response