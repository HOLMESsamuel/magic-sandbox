from .player import Player
from .card import Card
from pydantic import BaseModel
import json
import uuid
import random
import os

class GameState(BaseModel):
    players : list[Player] = []
    max_z_index : int = 1
    alert_message : str = ""
    river_cards : list[Card] = []
    pool : list[Card] = []
    type : str = "magic"
    scraped_card : list[Card] = []

    def remove_player(self, player_id):
        for player in self.players:
            if player.name == player_id:
                self.players.remove(player)
                break

    def add_player_if_not_exist(self, player_name, type):
        for player in self.players:
            if player.name == player_name:
                return
        player_index = len(self.players)
        player = Player(name=player_name, index=player_index)
        if type == "sr":
            player.deck.initialize_sr_deck()
            player.score = 50
        self.players.append(player)

    def get_player(self, player_name):
        for player in self.players:
            if player.name == player_name:
                return player
        return None

    def throw_dice(self, player : Player, dice_result, dice_value):
        self.alert_message = player.name + " threw a dice: " + str(dice_result) + "/" + str(dice_value)

    def move_card_from_board_to_hand(self, cardId, target_player : Player):
        for player in self.players:
            if player.board:
                card = player.board.pop_card(cardId)
                if card:
                    card.untap()
                    target_player.hand.cards.append(card)
                    break

    def move_card_from_hand_to_hand(self, player : Player, cardId, target_player : Player):
        if player.hand:
            card = player.hand.pop_card(cardId)
            if card:
                target_player.hand.cards.append(card)

    def move_card_from_graveyard_to_hand(self, player : Player, cardId, target_player : Player):
        card = player.graveyard.pop_card(cardId)
        if card:
            target_player.hand.cards.append(card)

    def move_card_from_exile_to_hand(self, player : Player, cardId, target_player : Player):
        card = player.exile.pop_card(cardId)
        if card:
            target_player.hand.cards.append(card)

    def move_card_to_graveyard(self, player : Player, cardId, target_player : Player):
        card = player.pop_card(cardId)
        card.tapped = False
        if card:
            target_player.graveyard.cards.append(card)

    def move_card_to_exile(self, player : Player, cardId, target_player : Player):
        card = player.pop_card(cardId)
        card.tapped = False
        if card:
            target_player.exile.cards.append(card)

    def initialize_sr_game(self):
        json_file = os.path.join(os.path.dirname(__file__), "cards.json")
        with open(json_file, "r") as f:
            data = json.load(f)

            for card in data.get("cards", []):
                for i in range(card['number']):
                    self.pool.append(Card(id=str(uuid.uuid4()), image="local", name=card['name'], horizontal=card['horizontal'], types=[card["type"]]))
            
            random.shuffle(self.pool)
            for i in range(5):
                self.river_cards.append(self.pool.pop(0))
            self.river_cards.append(Card(id=str(uuid.uuid4()), image="local", name="Explorer", types=["ship"]))


