from typing import List
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
        if player.deck :
            player.draw_commander()
            player.deck.shuffle()
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
    
    async def move_card_from_board_to_hand(self, playerId: str, roomId: str, cardIds: List[str], targetPlayerId: str):
        game_state : GameState = state_manager.get_group_state(roomId)
        target_player : Player = game_state.get_player(targetPlayerId)
        for cardId in cardIds:
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
    
    async def tap_cards(self, playerId: str, roomId: str, cardIds: List[str]):
        game_state : GameState = state_manager.get_group_state(roomId)
        player : Player = game_state.get_player(playerId)
        for cardId in cardIds:
            player.board.get_card(cardId).tap()
        await websocket_manager.broadcast(roomId, game_state)
        return {"message": playerId + " room " + roomId + " tap cards"}
    
    async def untap_cards(self, playerId: str, roomId: str, cardIds: List[str]):
        game_state : GameState = state_manager.get_group_state(roomId)
        player : Player = game_state.get_player(playerId)
        for cardId in cardIds:
            player.board.get_card(cardId).untap()
        await websocket_manager.broadcast(roomId, game_state)
        return {"message": playerId + " room " + roomId + " untap cards"}
    
    async def flip_cards(self, playerId: str, roomId: str, cardIds: List[str]):
        game_state : GameState = state_manager.get_group_state(roomId)
        player : Player = game_state.get_player(playerId)

        for cardId in cardIds:
            player.get_card(cardId).flip()

        await websocket_manager.broadcast(roomId, game_state)
        return {"message": playerId + " room " + roomId + " flipped cards"}
    
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
    
    async def update_card_counter(self, playerId: str, roomId: str, cardId: str, counter: int):
        game_state : GameState = state_manager.get_group_state(roomId)
        player : Player = game_state.get_player(playerId)
        player.update_card_counter(cardId, counter)
        await websocket_manager.broadcast(roomId, game_state)
        return {"message": playerId + " room " + roomId + " update " + cardId}
    
    async def copy_card(self, playerId: str, roomId: str, cardId: str):
        game_state : GameState = state_manager.get_group_state(roomId)
        player : Player = game_state.get_player(playerId)
        player.copy_card(cardId, game_state.max_z_index)
        game_state.max_z_index += 1
        await websocket_manager.broadcast(roomId, game_state)
        return {"message": playerId + " room " + roomId + " copy " + cardId}
    
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
    
    async def move_card_to_deck(self, playerId: str, roomId: str, cardIds: List[str], cardPosition: int):
        game_state : GameState = state_manager.get_group_state(roomId)
        player : Player = game_state.get_player(playerId)
        for cardId in cardIds:
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
    
    async def copy_token(self, playerId: str, roomId: str, id: str):
        game_state : GameState = state_manager.get_group_state(roomId)
        player : Player = game_state.get_player(playerId)
        player.copy_token(tokenId=id)
        await websocket_manager.broadcast(roomId, game_state)
        return {"message": playerId + " room " + roomId + " token copied"}
    
    async def move_card_to_graveyard(self, playerId: str, roomId: str, cardIds: List[str], tokenIds: List[str], targetPlayerId: str):
        game_state : GameState = state_manager.get_group_state(roomId)
        player : Player = game_state.get_player(playerId)
        target_player : Player = game_state.get_player(targetPlayerId)
        for cardId in cardIds:
            game_state.move_card_to_graveyard(player, cardId, target_player)
        for tokenId in tokenIds:
            player.delete_token(tokenId=tokenId)
        await websocket_manager.broadcast(roomId, game_state)
        return {"message": playerId + " room " + roomId + " card move to graveyard"}
    
    async def move_card_to_exile(self, playerId: str, roomId: str, cardIds: List[str], tokenIds: List[str], targetPlayerId: str):
        game_state : GameState = state_manager.get_group_state(roomId)
        player : Player = game_state.get_player(playerId)
        target_player : Player = game_state.get_player(targetPlayerId)
        for cardId in cardIds:
            game_state.move_card_to_exile(player, cardId, target_player)
        for tokenId in tokenIds:
            player.delete_token(tokenId=tokenId)
        await websocket_manager.broadcast(roomId, game_state)
        return {"message": playerId + " room " + roomId + " card move to graveyard"}
    
    async def move_card_from_graveyard_to_hand(self, playerId: str, roomId: str, card_id: str, targetPlayerId: str):
        game_state : GameState = state_manager.get_group_state(roomId)
        player : Player = game_state.get_player(playerId)
        target_player : Player = game_state.get_player(targetPlayerId)
        game_state.move_card_from_graveyard_to_hand(player, card_id, target_player)
        await websocket_manager.broadcast(roomId, game_state)
        return {"message": playerId + " room " + roomId + " card moved from graveyard to hand"}
    
    async def move_card_from_exile_to_hand(self, playerId: str, roomId: str, card_id: str, targetPlayerId: str):
        game_state : GameState = state_manager.get_group_state(roomId)
        player : Player = game_state.get_player(playerId)
        target_player : Player = game_state.get_player(targetPlayerId)
        game_state.move_card_from_exile_to_hand(player, card_id, target_player)
        await websocket_manager.broadcast(roomId, game_state)
        return {"message": playerId + " room " + roomId + " card moved from graveyard to hand"}
    
    async def add_player_background(self, roomId: str, playerId: str, file_path: str, width: int, height: int):
        game_state : GameState = state_manager.get_group_state(roomId)
        player : Player = game_state.get_player(playerId)
        player.add_background(file_path, width, height)
        await websocket_manager.broadcast(roomId, game_state)
        return {"message": playerId + " room " + roomId + " added a background"}
    
    async def remove_player_background(self, roomId: str, playerId: str):
        game_state : GameState = state_manager.get_group_state(roomId)
        player : Player = game_state.get_player(playerId)
        player.remove_background()
        await websocket_manager.broadcast(roomId, game_state)
        return {"message": playerId + " room " + roomId + " removed a background"}
    
    async def reveal_deck_first_card(self, roomId: str, playerId: str):
        game_state : GameState = state_manager.get_group_state(roomId)
        player : Player = game_state.get_player(playerId)
        player.deck.toggle_first_card_visibility()
        await websocket_manager.broadcast(roomId, game_state)
        return {"message": playerId + " room " + roomId + " reveal the first card of the deck"}
    
    async def move_card_from_river_to_graveyard(self, roomId: str, playerId: str, cardId: str):
        game_state : GameState = state_manager.get_group_state(roomId)
        player : Player = game_state.get_player(playerId)
        for index, card in enumerate(game_state.river_cards):
            if card.id == cardId:
                new_card = game_state.river_cards.pop(index)
                player.graveyard.cards.append(new_card)
                if card.name == "Explorer":
                    game_state.river_cards.insert(index, Card(id=str(uuid.uuid4()), image="local", name="Explorer"))
                else:
                    game_state.river_cards.insert(index, game_state.pool.pop(0))
        await websocket_manager.broadcast(roomId, game_state)
        return {"message": playerId + " room " + roomId + " took " + cardId + " from river"}
    
    async def mix_graveyard_to_deck(self, playerId, roomId):
        game_state : GameState = state_manager.get_group_state(roomId)
        player : Player = game_state.get_player(playerId)
        player.deck.cards.extend(player.graveyard.cards)
        player.deck.shuffle()
        player.graveyard.cards.clear()
        await websocket_manager.broadcast(roomId, game_state)
        return {"message": playerId + " room " + roomId + " mixed his graveyard to deck"}
    
    async def discard_board(self, playerId, roomId):
        game_state : GameState = state_manager.get_group_state(roomId)
        player : Player = game_state.get_player(playerId)
        player.graveyard.cards.extend(player.board.cards)
        player.board.cards.clear()
        await websocket_manager.broadcast(roomId, game_state)
        return {"message": playerId + " room " + roomId + " discarded his cards"}
    
    async def draw_5(self, playerId, roomId):
        game_state : GameState = state_manager.get_group_state(roomId)
        player : Player = game_state.get_player(playerId)
        for i in range(5):
            if len(player.deck.cards) > 0:
                player.draw_card()
            else:
                player.deck.cards.extend(player.graveyard.cards)
                player.deck.shuffle()
                player.graveyard.cards.clear()
                player.draw_card()
        await websocket_manager.broadcast(roomId, game_state)
        return {"message": playerId + " room " + roomId + " draw 5 cards"}
    