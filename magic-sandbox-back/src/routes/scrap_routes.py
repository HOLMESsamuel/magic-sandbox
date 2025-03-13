from typing import List
from fastapi import APIRouter, Body
from pydantic import BaseModel

from ..services.game_service import GameService

router = APIRouter()
game_service = GameService()

class CardIds(BaseModel):
    cardIds: List[str]

@router.put("/room/{roomId}/player/{playerId}/scrap/card/{cardId}/hand")
async def move_card_from_scrap_to_hand(roomId: str, playerId: str, cardId: str):
    response = await game_service.move_card_from_scrap_to_hand(roomId, playerId, cardId)
    return response

