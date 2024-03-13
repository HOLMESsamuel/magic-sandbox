import random
from pydantic import BaseModel
from .card import Card

class Deck(BaseModel):
    cards : list[Card] = []

    def shuffle(self):
        random.shuffle(self.cards)

    def reset(self):
        self.cards = []
