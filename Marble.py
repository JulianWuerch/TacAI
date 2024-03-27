class Marble:

    position: int
    activated: bool
    trixActivated: bool
    index: int

    def __init__(self, index: int):
        """
        Constructor of Marble.
        """
        self.position = 0
        self.activated = False
        self.index = index
        self.trixActivated = False