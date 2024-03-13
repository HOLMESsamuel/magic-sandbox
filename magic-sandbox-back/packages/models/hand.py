from pydantic import BaseModel
from .card import Card

class Hand(BaseModel):
    cards : list[Card] = []

    def reset(self):
        self.cards = []

    def get_card(self, cardId) -> Card:
        for card in self.cards:
            if card.id == cardId:
                return card
        return None
