from typing import List
from fastapi import APIRouter, Body
from pydantic import BaseModel

from ..services.game_service import GameService

router = APIRouter()
game_service = GameService()

class CardIds(BaseModel):
    cardIds: List[str]

@router.patch("/room/{roomId}/player/{playerId}/card/{cardId}/tap")
async def tap_card(playerId: str, roomId: str, cardId: str):
    response = await game_service.tap_card(playerId, roomId, cardId)
    return response

@router.patch("/room/{roomId}/player/{playerId}/card/{cardId}/untap")
async def untap_card(playerId: str, roomId: str, cardId: str):
    response = await game_service.untap_card(playerId, roomId, cardId)
    return response

@router.patch("/room/{roomId}/player/{playerId}/card/flip")
async def flip_cards(playerId: str, roomId: str, body: CardIds = Body(...)):
    response = await game_service.flip_cards(playerId, roomId, body.cardIds)
    return response

@router.put("/room/{roomId}/player/{playerId}/card/{cardId}/play")
async def play_card(playerId: str, roomId: str, cardId: str, position: dict):
    response = await game_service.play_card(playerId, roomId, cardId, position)
    return response

@router.put("/room/{roomId}/player/{playerId}/card/{cardId}/copy")
async def copy_card(playerId: str, roomId: str, cardId: str):
    response = await game_service.copy_card(playerId, roomId, cardId)
    return response