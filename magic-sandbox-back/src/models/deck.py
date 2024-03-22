import random
from pydantic import BaseModel
from .card import Card
from.card_container_abstract import CardContainerAbstract

class Deck(BaseModel, CardContainerAbstract):
    cards : list[Card] = []

    def shuffle(self):
        random.shuffle(self.cards)
