from Player import Player


class Game:
    
    roundCounter: int
    players: Player

    def __init__(self):
        self.roundCounter = 0