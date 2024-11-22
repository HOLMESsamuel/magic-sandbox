from pydantic import BaseModel
from .card import Card
from .card_container_abstract import CardContainerAbstract

class Exile(BaseModel, CardContainerAbstract):
    cards : list[Card] = []