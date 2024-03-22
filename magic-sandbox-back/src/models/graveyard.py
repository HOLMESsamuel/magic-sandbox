from pydantic import BaseModel
from .card import Card
from .card_container_abstract import CardContainerAbstract

class Graveyard(BaseModel, CardContainerAbstract):
    cards : list[Card] = []