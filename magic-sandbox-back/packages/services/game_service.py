from .websocket_manager import WebSocketManager
from .state_manager import StateManager
from ..models.game_state import *


state_manager = StateManager()
websocket_manager = WebSocketManager()

class GameService:

    async def mill_card(self, playerId: str, roomId: str): 
        move_card_from_deck_to_board(get_player_from_game_state(state_manager.get_group_state(roomId), playerId))
        await websocket_manager.broadcast(roomId, state_manager.get_group_state(roomId))
        return {"message": "Deck milled for player " + playerId + " room " + roomId}
    
    async def draw_card(self, playerId: str, roomId: str): 
        move_card_from_deck_to_hand(get_player_from_game_state(state_manager.get_group_state(roomId), playerId))
        await websocket_manager.broadcast(roomId, state_manager.get_group_state(roomId))
        return {"message": playerId + " room " + roomId + " draw a card"}
    
    async def update_score(self, playerId: str, roomId: str, score: int):
        update_player_score(get_player_from_game_state(state_manager.get_group_state(roomId), playerId), score)
        await websocket_manager.broadcast(roomId, state_manager.get_group_state(roomId))
        return {"message": playerId + " room " + roomId + " has " + str(score)}