from fastapi import APIRouter

from ..services.game_service import GameService

router = APIRouter()
game_service = GameService()

@router.patch("/room/{roomId}/player/{playerId}/card/{cardId}/tap")
async def tap_card(playerId: str, roomId: str, cardId: str):
    response = await game_service.tap_card(playerId, roomId, cardId)
    return response

@router.patch("/room/{roomId}/player/{playerId}/card/{cardId}/untap")
async def untap_card(playerId: str, roomId: str, cardId: str):
    response = await game_service.untap_card(playerId, roomId, cardId)
    return response

@router.patch("/room/{roomId}/player/{playerId}/card/{cardId}/flip")
async def flip_card(playerId: str, roomId: str, cardId: str):
    response = await game_service.flip_card(playerId, roomId, cardId)
    return response

@router.put("/room/{roomId}/player/{playerId}/card/{cardId}/play")
async def play_card(playerId: str, roomId: str, cardId: str, position: dict):
    response = await game_service.play_card(playerId, roomId, cardId, position)
    return response