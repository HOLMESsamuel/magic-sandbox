from .websocket_manager import WebSocketManager
from .state_manager import StateManager
from ..models.game_state import *
from ..models import deck
from ..models import player
import random


state_manager = StateManager()
websocket_manager = WebSocketManager()

class GameService:

    async def add_deck(self, playerId: str, roomId: str, deck: deck): 
        game_state : GameState = state_manager.get_group_state(roomId)
        player : Player = game_state.get_player(playerId)
        player.deck = deck
        await websocket_manager.broadcast(roomId, game_state)
        return {"message": "Deck added for player " + playerId + " room " + roomId}
    
    async def throw_dice(self, playerId: str, roomId: str, dice_value: int):
        dice_result = random.randint(1, dice_value)
        game_state : GameState = state_manager.get_group_state(roomId)
        player : Player = game_state.get_player(playerId)
        game_state.throw_dice(player, dice_result, dice_value)
        await websocket_manager.broadcast(roomId, game_state)
        return {"message": "Player " + playerId + " room " + roomId + " threw a dice: " + str(dice_result) + "/" + str(dice_value)}

    async def mill_card(self, playerId: str, roomId: str): 
        game_state : GameState = state_manager.get_group_state(roomId)
        player : Player = game_state.get_player(playerId)
        player.mill_card()
        await websocket_manager.broadcast(roomId, game_state)
        return {"message": "Deck milled for player " + playerId + " room " + roomId}
    
    async def reset(self, playerId: str, roomId: str): 
        game_state : GameState = state_manager.get_group_state(roomId)
        player : Player = game_state.get_player(playerId)
        player.reset()
        await websocket_manager.broadcast(roomId, game_state)
        return {"message": "Deck and board reset for " + playerId + " room " + roomId}
    
    async def draw_card(self, playerId: str, roomId: str): 
        game_state : GameState = state_manager.get_group_state(roomId)
        player : Player = game_state.get_player(playerId)
        player.draw_card()
        await websocket_manager.broadcast(roomId, game_state)
        return {"message": playerId + " room " + roomId + " draw a card"}
    
    async def move_card_from_deck_to_hand(self, playerId: str, roomId: str, cardId: str):
        game_state : GameState = state_manager.get_group_state(roomId)
        player : Player = game_state.get_player(playerId)
        player.move_card_from_deck_to_hand(cardId)
        await websocket_manager.broadcast(roomId, game_state)
        return {"message": playerId + " room " + roomId + " card moved from deck to hand"}
    
    async def move_card_from_board_to_hand(self, playerId: str, roomId: str, cardId: str, targetPlayerId: str):
        game_state : GameState = state_manager.get_group_state(roomId)
        target_player : Player = game_state.get_player(targetPlayerId)
        game_state.move_card_from_board_to_hand(cardId, target_player)
        await websocket_manager.broadcast(roomId, game_state)
        return {"message": playerId + " room " + roomId + " card moved from board to hand"}
    
    async def move_card_from_hand_to_hand(self, playerId: str, roomId: str, cardId: str, targetPlayerId: str):
        game_state : GameState = state_manager.get_group_state(roomId)
        player : Player = game_state.get_player(playerId)
        target_player : Player = game_state.get_player(targetPlayerId)
        game_state.move_card_from_hand_to_hand(player, cardId, target_player)
        await websocket_manager.broadcast(roomId, game_state)
        return {"message": playerId + " room " + roomId + " card moved from board to hand"}
    
    async def shuffle_deck(self, playerId: str, roomId: str):
        game_state : GameState = state_manager.get_group_state(roomId)
        player : Player = game_state.get_player(playerId)
        player.deck.shuffle()
        await websocket_manager.broadcast(roomId, game_state)
        return {"message": playerId + " room " + roomId + " deck shuffled " }
    
    async def update_score(self, playerId: str, roomId: str, score: int):
        game_state : GameState = state_manager.get_group_state(roomId)
        player : Player = game_state.get_player(playerId)
        player.score = score
        await websocket_manager.broadcast(roomId, game_state)
        return {"message": playerId + " room " + roomId + " has " + str(score)}
    
    async def tap_card(self, playerId: str, roomId: str, cardId: str):
        game_state : GameState = state_manager.get_group_state(roomId)
        player : Player = game_state.get_player(playerId)
        player.board.get_card(cardId).tap()
        await websocket_manager.broadcast(roomId, game_state)
        return {"message": playerId + " room " + roomId + " tap " + cardId}
    
    async def untap_card(self, playerId: str, roomId: str, cardId: str):
        game_state : GameState = state_manager.get_group_state(roomId)
        player : Player = game_state.get_player(playerId)
        player.board.get_card(cardId).untap()
        await websocket_manager.broadcast(roomId, game_state)
        return {"message": playerId + " room " + roomId + " untap " + cardId}
    
    async def flip_card(self, playerId: str, roomId: str, cardId: str):
        game_state : GameState = state_manager.get_group_state(roomId)
        player : Player = game_state.get_player(playerId)
        player.get_card(cardId).flip()
        await websocket_manager.broadcast(roomId, game_state)
        return {"message": playerId + " room " + roomId + " flip " + cardId}
    
    async def tap_token(self, playerId: str, roomId: str, tokenId: str):
        game_state : GameState = state_manager.get_group_state(roomId)
        player : Player = game_state.get_player(playerId)
        player.board.get_token(tokenId).tap()
        await websocket_manager.broadcast(roomId, game_state)
        return {"message": playerId + " room " + roomId + " tap " + tokenId}
    
    async def untap_token(self, playerId: str, roomId: str, tokenId: str):
        game_state : GameState = state_manager.get_group_state(roomId)
        player : Player = game_state.get_player(playerId)
        player.board.get_token(tokenId).untap()
        await websocket_manager.broadcast(roomId, game_state)
        return {"message": playerId + " room " + roomId + " untap " + tokenId}
    
    async def play_card(self, playerId: str, roomId: str, cardId: str, position: dict):
        game_state : GameState = state_manager.get_group_state(roomId)
        player : Player = game_state.get_player(playerId)
        player.play_card(cardId, position, game_state.max_z_index)
        game_state.max_z_index += 1
        await websocket_manager.broadcast(roomId, game_state)
        return {"message": playerId + " room " + roomId + " play " + cardId}
    
    async def detap_all(self, playerId: str, roomId: str):
        game_state : GameState = state_manager.get_group_state(roomId)
        player : Player = game_state.get_player(playerId)
        player.board.detap_all()
        await websocket_manager.broadcast(roomId, game_state)
        return {"message": playerId + " room " + roomId + " detap all"}
    
    async def mulligan(self, playerId: str, roomId: str):
        game_state : GameState = state_manager.get_group_state(roomId)
        player : Player = game_state.get_player(playerId)
        player.mulligan()
        await websocket_manager.broadcast(roomId, game_state)
        return {"message": playerId + " room " + roomId + " mulligan"}
    
    async def move_card_to_deck(self, playerId: str, roomId: str, cardId: str, cardPosition: int):
        game_state : GameState = state_manager.get_group_state(roomId)
        player : Player = game_state.get_player(playerId)
        player.move_card_to_deck(cardId, cardPosition)
        await websocket_manager.broadcast(roomId, game_state)
        return {"message": playerId + " room " + roomId + " card " + cardId + " moved to deck on position " + str(cardPosition)}
    
    async def create_token(self, playerId: str, roomId: str, text: str, type: str, copy: int):
        game_state : GameState = state_manager.get_group_state(roomId)
        player : Player = game_state.get_player(playerId)
        for _ in range(copy):
            player.create_token(text, type, game_state.max_z_index)
            game_state.max_z_index += 1
        await websocket_manager.broadcast(roomId, game_state)
        return {"message": playerId + " room " + roomId + " token created"}
    
    async def delete_token(self, playerId: str, roomId: str, id: str):
        game_state : GameState = state_manager.get_group_state(roomId)
        player : Player = game_state.get_player(playerId)
        player.delete_token(tokenId=id)
        await websocket_manager.broadcast(roomId, game_state)
        return {"message": playerId + " room " + roomId + " token deleted"}
    
    async def modify_token(self, playerId: str, roomId: str, id: str, text: str, type: str):
        game_state : GameState = state_manager.get_group_state(roomId)
        player : Player = game_state.get_player(playerId)
        player.modify_token(tokenId=id, text=text, type=type)
        await websocket_manager.broadcast(roomId, game_state)
        return {"message": playerId + " room " + roomId + " token deleted"}
    
    async def move_card_to_graveyard(self, playerId: str, roomId: str, cardId: str, targetPlayerId: str):
        game_state : GameState = state_manager.get_group_state(roomId)
        player : Player = game_state.get_player(playerId)
        target_player : Player = game_state.get_player(targetPlayerId)
        game_state.move_card_to_graveyard(player, cardId, target_player)
        await websocket_manager.broadcast(roomId, game_state)
        return {"message": playerId + " room " + roomId + " card move to graveyard"}
    
    async def move_card_from_graveyard_to_hand(self, playerId: str, roomId: str, card_id: str, targetPlayerId: str):
        game_state : GameState = state_manager.get_group_state(roomId)
        player : Player = game_state.get_player(playerId)
        target_player : Player = game_state.get_player(targetPlayerId)
        game_state.move_card_from_graveyard_to_hand(player, card_id, target_player)
        await websocket_manager.broadcast(roomId, game_state)
        return {"message": playerId + " room " + roomId + " card moved from graveyard to hand"}