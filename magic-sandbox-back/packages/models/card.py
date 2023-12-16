class Card:
    def __init__(self, id, name, type, image, position=None):
        self.id = id
        self.name = name
        self.type = type
        self.image = image
        self.position = position if position else {'x': 2000, 'y': 200}

    