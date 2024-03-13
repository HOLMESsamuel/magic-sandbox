from pydantic import BaseModel
from .card import Card
from .token import Token

class Board(BaseModel):
  cards : list[Card] = []
  tokens : list[Token] = [] 

  def reset(self):
    self.cards = []
    self.tokens = []

  def get_card(self, cardId) -> Card:
    for card in self.cards:
        if card.id == cardId:
            return card
    return None

  def get_token(self, tokenId) -> Token:
    for token in self.tokens:
        if token.id == tokenId:
            return token
    return None

  def detap_all(self):
    for card in self.cards:
        card.untap()
    for token in self.tokens:
        token.untap()