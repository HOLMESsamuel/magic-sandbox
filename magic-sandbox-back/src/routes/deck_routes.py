from fastapi import APIRouter
from ..services import WebScraperService
from ..services import GameService

router = APIRouter()
game_service = GameService()
web_scraper_service = WebScraperService()

@router.put("/room/{roomId}/player/{playerId}/deck/mill")
async def mill_deck(playerId: str, roomId: str):
    response = await game_service.mill_card(playerId, roomId)
    return response

@router.put("/room/{roomId}/player/{playerId}/deck/reset")
async def reset(playerId: str, roomId: str):
    response = await game_service.reset(playerId, roomId)
    return response

@router.put("/room/{roomId}/player/{playerId}/deck/draw")
async def draw_card(playerId: str, roomId: str):
    response = await game_service.draw_card(playerId, roomId)
    return response

@router.put("/room/{roomId}/player/{playerId}/deck/shuffle")
async def shuffle_deck(playerId: str, roomId: str):
    response = await game_service.shuffle_deck(playerId, roomId)
    return response

@router.put("/room/{roomId}/player/{playerId}/deck/reveal")
async def reveal_deck_first_card(playerId: str, roomId: str):
    response = await game_service.reveal_deck_first_card(roomId, playerId)
    return response

@router.put("/room/{roomId}/player/{playerId}/card/{cardId}/deck/{cardPosition}")
async def move_card_to_deck(playerId: str, roomId: str, cardId: str, cardPosition: int):
    response = await game_service.move_card_to_deck(playerId, roomId, cardId, cardPosition)
    return response