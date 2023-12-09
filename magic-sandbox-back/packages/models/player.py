class Player:
    def __init__(self, name, hand=None, deck=None, board=None):
        self.name = name
        self.hand = hand if hand is not None else []
        self.deck = deck if deck is not None else []
        self.board = board if board is not None else []

    def move_card_from_deck_to_board(self):
        if self.deck:
            card = self.deck.pop(0)  # Remove the first card from the deck
            self.board.append(card)  # Add the card to the board
        else:
            print("The deck is empty, no card to move.")

    @staticmethod
    def from_dict(player_dict):
        return Player(
            player_dict['name'],
            hand=player_dict.get('hand', []),
            deck=player_dict.get('deck', []),
            board=player_dict.get('board', [])
        )