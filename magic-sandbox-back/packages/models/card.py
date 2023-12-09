class Card:
    def __init__(self, id, name, type, image, position=None):
        self.id = id
        self.name = name
        self.type = type
        self.image = image
        self.position = position if position else {'x': 0, 'y': 0}

    