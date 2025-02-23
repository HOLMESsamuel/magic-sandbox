import random
from pydantic import BaseModel
from .card import Card
from.card_container_abstract import CardContainerAbstract
import uuid

class Deck(BaseModel, CardContainerAbstract):
    cards : list[Card] = []
    first_card_revealed : bool = False

    def shuffle(self):
        random.shuffle(self.cards)

    def toggle_first_card_visibility(self):
        self.first_card_revealed = not self.first_card_revealed

    def reset(self):
        super().reset()
        self.first_card_revealed = False

    def initialize_sr_deck(self):
        for i in range(8):
            id = str(uuid.uuid4())
            card : Card = Card(name="Scout", id=id, image="local")
            self.cards.append(card)
        for i in range(2):
            id = str(uuid.uuid4())
            card : Card = Card(name="Viper", id=id, image="local")
            self.cards.append(card)
        self.shuffle()


    
