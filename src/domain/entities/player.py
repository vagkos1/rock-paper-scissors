import uuid

class Player:
    def __init__(self, name: str, is_computer: bool = False):
        self.id = str(uuid.uuid4())
        self.name = name
        self.is_computer = is_computer