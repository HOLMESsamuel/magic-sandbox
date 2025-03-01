from typing import List
from fastapi import APIRouter, Body
from pydantic import BaseModel

from ..services.game_service import GameService

router = APIRouter()
game_service = GameService()

class CardIds(BaseModel):
    cardIds: List[str]

@router.put("/room/{roomId}/player/{playerId}/deck/card/{cardId}/hand")
async def move_card_from_deck_to_hand(playerId: str, roomId: str, cardId: str):
    response = await game_service.move_card_from_deck_to_hand(playerId, roomId, cardId)
    return response

@router.put("/room/{roomId}/player/{playerId}/board/card/hand/{targetPlayerId}")
async def move_card_from_board_to_hand(playerId: str, roomId: str, targetPlayerId: str, body: CardIds = Body(...)):
    response = await game_service.move_card_from_board_to_hand(playerId, roomId, body.cardIds, targetPlayerId)
    return response

@router.put("/room/{roomId}/player/{playerId}/hand/card/{cardId}/hand/{targetPlayerId}")
async def move_card_from_hand_to_hand(playerId: str, roomId: str, cardId: str, targetPlayerId: str):
    response = await game_service.move_card_from_hand_to_hand(playerId, roomId, cardId, targetPlayerId)
    return response

@router.put("/room/{roomId}/player/{playerId}/graveyard/card/{cardId}/hand/{targetPlayerId}")
async def move_card_from_graveyard_to_hand(playerId: str, roomId: str, cardId: str, targetPlayerId: str):
    response = await game_service.move_card_from_graveyard_to_hand(playerId, roomId, cardId, targetPlayerId)
    return response

@router.put("/room/{roomId}/player/{playerId}/exile/card/{cardId}/hand/{targetPlayerId}")
async def move_card_from_exile_to_hand(playerId: str, roomId: str, cardId: str, targetPlayerId: str):
    response = await game_service.move_card_from_exile_to_hand(playerId, roomId, cardId, targetPlayerId)
    return response

@router.put("/room/{roomId}/player/{playerId}/mulligan")
async def mulligan(playerId: str, roomId: str):
    response = await game_service.mulligan(playerId, roomId)
    return response

@router.put("/room/{roomId}/player/{playerId}/hand/draw5")
async def draw_5(playerId: str, roomId: str):
    response = await game_service.draw_5(playerId, roomId)
    return response