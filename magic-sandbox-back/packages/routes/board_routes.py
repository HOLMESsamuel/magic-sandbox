from fastapi import APIRouter

from ..services.game_service import GameService
    
router = APIRouter()
game_service = GameService()

@router.get("/room/{roomId}/player/{playerId}/dice/{diceValue}")
async def throw_dice(playerId: str, roomId: str, diceValue: int):
    dice_result = await game_service.throw_dice(playerId, roomId, diceValue)
    return dice_result

@router.put("/room/{roomId}/player/{playerId}/score/{score}")
async def update_score(playerId: str, roomId: str, score: int):
    response = await game_service.update_score(playerId, roomId, score)
    return response

@router.put("/room/{roomId}/player/{playerId}/board/detap")
async def detap_all(playerId: str, roomId: str):
    response = await game_service.detap_all(playerId, roomId)
    return response
