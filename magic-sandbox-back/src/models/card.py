from typing import List
from pydantic import BaseModel
from ..constants import DEFAULT_CARD_BACK_URL

class Card(BaseModel):
    id : str
    name : str
    image : str
    position : dict = {'x': 2000, 'y': 200}
    tapped : bool = False
    flipped : bool = False
    flip_image : str = DEFAULT_CARD_BACK_URL
    z_index : int = 2
    commander : bool  = False
    types : List[str] = []
    copy: bool = False

    def tap(self):
        self.tapped = True
    
    def untap(self):
        self.tapped = False

    def flip(self):
        self.flipped = not self.flipped