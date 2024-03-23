from fastapi import APIRouter
from ..services import GameService

router = APIRouter()
game_service = GameService()


@router.put("/room/{roomId}/player/{playerId}/card/{cardId}/graveyard/{targetPlayerId}")
async def move_card_to_graveyard(playerId: str, roomId: str, cardId: str, targetPlayerId: str):
    response = await game_service.move_card_to_graveyard(playerId, roomId, cardId, targetPlayerId)
    return response