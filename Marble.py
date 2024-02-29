class Marble:

    position: int
    activated: bool
    index: int

    def __init__(self, index: int):
        self.position = 0
        self.activated = False
        self.index = index