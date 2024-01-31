import random

class Deck:
    def __init__(self, cards):
        self.cards = cards

    # Convert all cards in the deck to dictionaries
    def cards_to_dict(self):
        return [card.to_dict() for card in self.cards]