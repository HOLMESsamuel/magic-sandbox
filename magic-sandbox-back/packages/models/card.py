class Card:
    def __init__(self, id, name, type, image, position=None, tapped=False, z_index=2):
        self.id = id
        self.name = name
        self.type = type
        self.image = image
        self.position = position if position else {'x': 2000, 'y': 200}
        self.tapped = tapped
        self.z_index = z_index

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'image': self.image,
            'position': self.position,
            'tapped': self.tapped,
            'z_index': self.z_index,
        }