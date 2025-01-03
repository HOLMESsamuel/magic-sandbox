from typing import List
from fastapi import APIRouter, Body
from pydantic import BaseModel
from ..services import GameService

router = APIRouter()
game_service = GameService()

class CardIds(BaseModel):
    cardIds: List[str]
    tokenIds: List[str]



@router.put("/room/{roomId}/player/{playerId}/exile/{targetPlayerId}")
async def move_card_to_exile(playerId: str, roomId: str, targetPlayerId: str, body: CardIds = Body(...)):
    response = await game_service.move_card_to_exile(playerId, roomId, body.cardIds, body.tokenIds, targetPlayerId)
    return response