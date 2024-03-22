from pydantic import BaseModel
from .card import Card
from .token import Token
from .card_container_abstract import CardContainerAbstract

class Board(BaseModel, CardContainerAbstract):
  cards : list[Card] = []
  tokens : list[Token] = [] 

  def reset(self):
    self.cards = []
    self.tokens = []

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