from .websocket_manager import WebSocketManager
from .state_manager import StateManager
from ..models.game_state import *
from ..models import deck


state_manager = StateManager()
websocket_manager = WebSocketManager()

class GameService:

    async def add_deck(self, playerId: str, roomId: str, deck: deck): 
        game_state = state_manager.get_group_state(roomId)
        add_deck(get_player_from_game_state(game_state, playerId), deck)
        await websocket_manager.broadcast(roomId, state_manager.get_group_state(roomId))
        return {"message": "Deck added for player " + playerId + " room " + roomId}
    
    async def throw_dice(self, playerId: str, roomId: str, dice_value: int):
        dice_result = random.randint(1, dice_value)
        game_state = state_manager.get_group_state(roomId)
        throw_dice(game_state, get_player_from_game_state(game_state, playerId), dice_result, dice_value)
        await websocket_manager.broadcast(roomId, state_manager.get_group_state(roomId))
        return {"message": "Player " + playerId + " room " + roomId + " threw a dice: " + str(dice_result) + "/" + str(dice_value)}

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
    
    async def move_card_from_deck_to_hand(self, playerId: str, roomId: str, cardId: str):
        move_card_from_deck_to_hand(get_player_from_game_state(state_manager.get_group_state(roomId), playerId), cardId)
        await websocket_manager.broadcast(roomId, state_manager.get_group_state(roomId))
        return {"message": playerId + " room " + roomId + " card moved from deck to hand"}
    
    async def move_card_from_board_to_hand(self, playerId: str, roomId: str, cardId: str, targetPlayerId: str):
        player = get_player_from_game_state(state_manager.get_group_state(roomId), playerId)
        target_player = get_player_from_game_state(state_manager.get_group_state(roomId), targetPlayerId)
        move_card_from_board_to_hand(player, cardId, target_player)
        await websocket_manager.broadcast(roomId, state_manager.get_group_state(roomId))
        return {"message": playerId + " room " + roomId + " card moved from board to hand"}
    
    async def move_card_from_hand_to_hand(self, playerId: str, roomId: str, cardId: str, targetPlayerId: str):
        player = get_player_from_game_state(state_manager.get_group_state(roomId), playerId)
        target_player = get_player_from_game_state(state_manager.get_group_state(roomId), targetPlayerId)
        move_card_from_hand_to_hand(player, cardId, target_player)
        await websocket_manager.broadcast(roomId, state_manager.get_group_state(roomId))
        return {"message": playerId + " room " + roomId + " card moved from board to hand"}
    
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
    
    async def tap_token(self, playerId: str, roomId: str, tokenId: str):
        tap_token(get_player_from_game_state(state_manager.get_group_state(roomId), playerId), tokenId)
        await websocket_manager.broadcast(roomId, state_manager.get_group_state(roomId))
        return {"message": playerId + " room " + roomId + " tap " + tokenId}
    
    async def untap_token(self, playerId: str, roomId: str, tokenId: str):
        untap_token(get_player_from_game_state(state_manager.get_group_state(roomId), playerId), tokenId)
        await websocket_manager.broadcast(roomId, state_manager.get_group_state(roomId))
        return {"message": playerId + " room " + roomId + " untap " + tokenId}
    
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
    
    async def move_card_to_deck(self, playerId: str, roomId: str, cardId: str, cardPosition: int):
        move_card_to_deck(get_player_from_game_state(state_manager.get_group_state(roomId), playerId), cardId, cardPosition)
        await websocket_manager.broadcast(roomId, state_manager.get_group_state(roomId))
        return {"message": playerId + " room " + roomId + " card " + cardId + " moved to deck on position " + str(cardPosition)}
    
    async def create_token(self, playerId: str, roomId: str, text: str, type: str):
        state = state_manager.get_group_state(roomId)
        player_index = get_player_index(state, playerId)
        create_token(get_player_from_game_state(state, playerId), text, type, state["max_z_index"], player_index)
        state["max_z_index"] += 1
        await websocket_manager.broadcast(roomId, state_manager.get_group_state(roomId))
        return {"message": playerId + " room " + roomId + " token created"}
    
    async def delete_token(self, playerId: str, roomId: str, id: str):
        delete_token(get_player_from_game_state(state_manager.get_group_state(roomId), playerId), id)
        await websocket_manager.broadcast(roomId, state_manager.get_group_state(roomId))
        return {"message": playerId + " room " + roomId + " token deleted"}
    
    async def modify_token(self, playerId: str, roomId: str, id: str, text: str, type: str):
        modify_token(get_player_from_game_state(state_manager.get_group_state(roomId), playerId), id, text, type)
        await websocket_manager.broadcast(roomId, state_manager.get_group_state(roomId))
        return {"message": playerId + " room " + roomId + " token deleted"}