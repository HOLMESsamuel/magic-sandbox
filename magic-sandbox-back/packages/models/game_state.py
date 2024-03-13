from .player import Player
from pydantic import BaseModel

class GameState(BaseModel):
    players : list[Player] = []
    max_z_index : int = 1
    alert_message : str = ""

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
                for index, card in enumerate(player.board.cards):
                    if card.id == cardId:
                        card = player.board.cards.pop(index)
                        print(card)
                        card.untap()
                        target_player.hand.cards.append(card)
                        break
            else:
                print("The board is empty, no card to move.")

    def move_card_from_hand_to_hand(self, player : Player, cardId, target_player : Player):
        if player.hand:
            for index, card in enumerate(player.hand):
                if card.id == cardId:
                    card = player.hand.cards.pop(index)
                    target_player.hand.cards.append(card)
                    break
        else:
            print("The hand is empty, no card to move.")


