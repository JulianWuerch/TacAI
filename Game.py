from typing import List
from Action import Action
from Player import Player


class Game:
    
    roundCounter: int
    PLAYER_COUNT = 4
    HAND_SIZE = 5
    players: List[Player] = []
    running: bool = False
    actionLog: List[Action] = []

    def __init__(self):
        self.roundCounter = 0
        self.actionLog = []
        self.players = []
        for i in range(self.PLAYER_COUNT):
            name = input(f"Player {i} name: ")
            type = input(f"Player {i} type: ")
            print("")
            self.players.append(Player(i, type, name))
        
        self.generateCardDeck()


    def start(self):
        self.running = True
        while self.running:

            self.mixCardDeck()
            self.dishCards()
            self.reportExitCard()
            self.tradeCards()

            winnerTeam = ""

            for round in range(self.HAND_SIZE):
                self.playRound(round)
                self.roundCounter += 1
                winnerTeam = self.checkWinCondition()

            if winnerTeam:
                self.celebrateTeam(winnerTeam)
                self.running = False


    def generateCardDeck(self):
        pass

    def mixCardDeck(self):
        pass

    def dishCards(self):
        pass

    def reportExitCard(self):
        pass

    def tradeCards(self):
        pass

    def playRound(self, round):
        print(f"---Round {round}---")

        for player in self.players:
            action = player.playCard()
            self.runAction(action)
            self.actionLog.append(action)


    def runAction(self, action: Action):
        pass

    def celebrateTeam(self, team: str):
        pass