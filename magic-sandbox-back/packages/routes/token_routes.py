from fastapi import APIRouter, Body
from pydantic import BaseModel

from ..services.game_service import GameService

class TokenData(BaseModel):
    text: str
    type: str
    copy: int

router = APIRouter()
game_service = GameService()

@router.post("/room/{roomId}/player/{playerId}/token")
async def create_token(playerId: str, roomId: str, token_data: TokenData = Body(...)):
    response = await game_service.create_token(playerId, roomId, token_data.text, token_data.type, token_data.copy)
    return response

@router.delete("/room/{roomId}/player/{playerId}/token/{id}")
async def delete_token(playerId: str, roomId: str, id: str):
    response = await game_service.delete_token(playerId, roomId, id)
    return response

@router.put("/room/{roomId}/player/{playerId}/token/{id}")
async def modify_token(playerId: str, roomId: str, id: str, token_data: TokenData = Body(...)):
    response = await game_service.modify_token(playerId, roomId, id, token_data.text, token_data.type)
    return response

@router.patch("/room/{roomId}/player/{playerId}/token/{tokenId}/tap")
async def tap_token(playerId: str, roomId: str, tokenId: str):
    response = await game_service.tap_token(playerId, roomId, tokenId)
    return response

@router.patch("/room/{roomId}/player/{playerId}/token/{tokenId}/untap")
async def untap_token(playerId: str, roomId: str, tokenId: str):
    response = await game_service.untap_token(playerId, roomId, tokenId)
    return response