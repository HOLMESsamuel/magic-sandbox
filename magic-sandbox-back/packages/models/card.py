class Card:
    def __init__(self, id, name, type, image, flip_image='', position=None, tapped=False, flipped=False, z_index=2):
        self.id = id
        self.name = name
        self.type = type
        self.image = image
        self.position = position if position else {'x': 2000, 'y': 200}
        self.tapped = tapped
        self.flipped = flipped
        self.flip_image = flip_image
        self.z_index = z_index

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'image': self.image,
            'position': self.position,
            'tapped': self.tapped,
            'flipped': self.flipped,
            'flip_image': self.flip_image,
            'z_index': self.z_index,
        }