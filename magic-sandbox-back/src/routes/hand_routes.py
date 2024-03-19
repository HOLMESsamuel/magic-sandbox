from fastapi import APIRouter

from ..services.game_service import GameService

router = APIRouter()
game_service = GameService()

@router.put("/room/{roomId}/player/{playerId}/deck/card/{cardId}/hand")
async def move_card_from_deck_to_hand(playerId: str, roomId: str, cardId: str):
    response = await game_service.move_card_from_deck_to_hand(playerId, roomId, cardId)
    return response

@router.put("/room/{roomId}/player/{playerId}/board/card/{cardId}/hand/{targetPlayerId}")
async def move_card_from_board_to_hand(playerId: str, roomId: str, cardId: str, targetPlayerId: str):
    response = await game_service.move_card_from_board_to_hand(playerId, roomId, cardId, targetPlayerId)
    return response

@router.put("/room/{roomId}/player/{playerId}/hand/card/{cardId}/hand/{targetPlayerId}")
async def move_card_from_hand_to_hand(playerId: str, roomId: str, cardId: str, targetPlayerId: str):
    response = await game_service.move_card_from_hand_to_hand(playerId, roomId, cardId, targetPlayerId)
    return response

@router.put("/room/{roomId}/player/{playerId}/mulligan")
async def mulligan(playerId: str, roomId: str):
    response = await game_service.mulligan(playerId, roomId)
    return response