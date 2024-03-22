from fastapi import APIRouter
from ..services import GameService

router = APIRouter()
game_service = GameService()


@router.put("/room/{roomId}/player/{playerId}/card/{cardId}/graveyard")
async def move_card_to_graveyard(playerId: str, roomId: str, cardId: str):
    response = await game_service.move_card_to_graveyard(playerId, roomId, cardId)
    return response