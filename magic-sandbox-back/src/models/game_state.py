from .player import Player
from .card import Card
from pydantic import BaseModel

class GameState(BaseModel):
    players : list[Player] = []
    max_z_index : int = 1
    alert_message : str = ""
    river_cards : list[Card] = []

    def remove_player(self, player_id):
        for player in self.players:
            if player.name == player_id:
                self.players.remove(player)
                break

    def add_player_if_not_exist(self, player_name):
        for player in self.players:
            if player.name == player_name:
                return
        player_index = len(self.players)
        self.players.append(Player(name=player_name, index=player_index))

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


