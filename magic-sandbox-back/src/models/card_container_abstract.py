from abc import ABC
from .card import Card


class CardContainerAbstract(ABC):
    
    def get_card(self, cardId) -> Card:
        for card in self.cards:
            if card.id == cardId:
                return card
        return None
    
    def pop_card(self, cardId) -> Card:
        for index, card in enumerate(self.cards):
            if card.id == cardId:
                return self.cards.pop(index)
    
    def reset(self):
        self.cards = []