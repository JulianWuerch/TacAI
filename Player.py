from typing import List

from Card import Card
from Enums import Action, PlayerType


class Player:
    ownID: int
    ownHandCards = []
    playerType = PlayerType.USER
    playedByAI = False
    playerName = ""

    def __init__(self, id: int, type: PlayerType, name: str = ""):
        self.ownID = id
        self.playerType = type
        self.playedByAI = not (type == PlayerType.USER)
        if name:
            self.playerName = name
        else:
            self.playerName = f"Bot{id}"

    def playCard() -> Action:
        pass

    def getID(self) -> int:
        return self.ownID
    
    def setID(self, newID) -> None:
        self.ownID = newID
    
    def getHandCards(self) -> List:
        return self.ownHandCards
    
    def setHandCards(self, newHandCards) -> None:
        self.ownHandCards = newHandCards

    def removeSingleCard(self, cardToRemove) -> None:
        self.ownHandCards.remove(cardToRemove)
    
    def getSingleCard(self, index) -> Card:
        return self.ownHandCards[index]
    
    def addSingleCard(self, cardToAdd) -> None:
        self.ownHandCards.append(cardToAdd)

    def setPlayedByAI(self, playedByAI) -> None:
        self.playedByAI = playedByAI

    def isPlayedByAI(self) -> bool:
        return self.playedByAI