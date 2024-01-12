from .websocket_manager import WebSocketManager
from .state_manager import StateManager
from ..models.game_state import *


state_manager = StateManager()
websocket_manager = WebSocketManager()

class GameService:

    async def mill_card(self, playerId: str, roomId: str): 
        game_state = state_manager.get_group_state(roomId)
        player_index = get_player_index(game_state, playerId)
        mill_card(get_player_from_game_state(game_state, playerId), player_index)
        await websocket_manager.broadcast(roomId, state_manager.get_group_state(roomId))
        return {"message": "Deck milled for player " + playerId + " room " + roomId}
    
    async def reset(self, playerId: str, roomId: str): 
        game_state = state_manager.get_group_state(roomId)
        reset_player(get_player_from_game_state(game_state, playerId))
        await websocket_manager.broadcast(roomId, state_manager.get_group_state(roomId))
        return {"message": "Deck and board reset for " + playerId + " room " + roomId}
    
    async def draw_card(self, playerId: str, roomId: str): 
        draw_card(get_player_from_game_state(state_manager.get_group_state(roomId), playerId))
        await websocket_manager.broadcast(roomId, state_manager.get_group_state(roomId))
        return {"message": playerId + " room " + roomId + " draw a card"}
    
    async def add_card_to_hand(self, playerId: str, roomId: str, cardId: str):
        move_card_from_deck_to_hand(get_player_from_game_state(state_manager.get_group_state(roomId), playerId), cardId)
        await websocket_manager.broadcast(roomId, state_manager.get_group_state(roomId))
        return {"message": playerId + " room " + roomId + " card moved to hand"}
    
    async def shuffle_deck(self, playerId: str, roomId: str):
        shuffle_deck(get_player_from_game_state(state_manager.get_group_state(roomId), playerId))
        await websocket_manager.broadcast(roomId, state_manager.get_group_state(roomId))
        return {"message": playerId + " room " + roomId + " deck shuffled " }
    
    async def update_score(self, playerId: str, roomId: str, score: int):
        update_player_score(get_player_from_game_state(state_manager.get_group_state(roomId), playerId), score)
        await websocket_manager.broadcast(roomId, state_manager.get_group_state(roomId))
        return {"message": playerId + " room " + roomId + " has " + str(score)}
    
    async def tap_card(self, playerId: str, roomId: str, cardId: str):
        tap_card(get_player_from_game_state(state_manager.get_group_state(roomId), playerId), cardId)
        await websocket_manager.broadcast(roomId, state_manager.get_group_state(roomId))
        return {"message": playerId + " room " + roomId + " tap " + cardId}
    
    async def untap_card(self, playerId: str, roomId: str, cardId: str):
        untap_card(get_player_from_game_state(state_manager.get_group_state(roomId), playerId), cardId)
        await websocket_manager.broadcast(roomId, state_manager.get_group_state(roomId))
        return {"message": playerId + " room " + roomId + " untap " + cardId}
    
    async def play_card(self, playerId: str, roomId: str, cardId: str, position: dict):
        state = state_manager.get_group_state(roomId)
        play_card(get_player_from_game_state(state, playerId), cardId, position, state["max_z_index"])
        state["max_z_index"] += 1
        await websocket_manager.broadcast(roomId, state_manager.get_group_state(roomId))
        return {"message": playerId + " room " + roomId + " play " + cardId}
    
    async def detap_all(self, playerId: str, roomId: str):
        detap_all(get_player_from_game_state(state_manager.get_group_state(roomId), playerId))
        await websocket_manager.broadcast(roomId, state_manager.get_group_state(roomId))
        return {"message": playerId + " room " + roomId + " detap all"}
    
    async def mulligan(self, playerId: str, roomId: str):
        mulligan(get_player_from_game_state(state_manager.get_group_state(roomId), playerId))
        await websocket_manager.broadcast(roomId, state_manager.get_group_state(roomId))
        return {"message": playerId + " room " + roomId + " mulligan"}