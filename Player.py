from typing import List

from Card import Card


class Player:
    ownID: int
    ownHandCards = []
    playedByAI = False

    def __init__(self, id: int, playedByAI: bool):
        self.ownID = id
        self.playedByAI = playedByAI

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