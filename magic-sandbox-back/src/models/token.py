from pydantic import BaseModel

class Token(BaseModel):
    id : str
    text : str
    position : dict = {'x': 2000, 'y': 200}
    tapped : bool = False
    z_index : int = 2
    type : str

    def tap(self):
        self.tapped = True
    
    def untap(self):
        self.tapped = False