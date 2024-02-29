from random import Random
from typing import List
from Action import Action

from Card import Card
from Enums import PlayerType
from Marble import Marble


class Player:

    ownID: int
    playerType: PlayerType = PlayerType.USER
    playedByAI: bool = False
    _playerName: str = ""
    _ownHandCards: List[Card] = []
    _signalOpeningCard: bool = False
    _marbles: List[Marble]


    def __init__(self, id: int, type: PlayerType, name: str = ""):
        """
        Constructor of a player.
        """

        self.ownID = id
        self.playerType = type
        self.playedByAI = not (type == PlayerType.USER)

        if name:
            self._playerName = name
        else:
            self._playerName = f"Bot{id}"


    def playCard(self) -> Action:
        """
        Lets the player choose which card he wants to play.
        If the player is controled by an AI the AI chooses the card.

        :return: The action the player wants to take.
        """

        if self.isPlayedByAI:
            return self.ai.getAction()
        
        else:
            print(f"---Player {self.playerName}---")
            self.printHandCards()
            cardIndex = -1
            print("Play a card")

            while cardIndex < 0 or cardIndex >= len(self.getHandCards()):
                cardIndex = int(print(f"[1-{len(self.getHandCards())}]")) - 1
            
            chosenCard = self.getHandCards().pop(cardIndex)

            return chosenCard.executeCard()


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
    
    def setSignalOpeningCard(self, signalState: bool) -> None:
        self.signalOpeningCard = signalState

    def signalOpeningCardState(self) -> bool:
        return self.signalOpeningCard
    
    def setMarbles(self, marbles: List[Marble]) -> None:
        self._marbles = marbles

    def getMarbles(self) -> List[Marble]:
        return self._marbles
    
    def setMarblePosition(self, marbleIndex: int, position: int) -> None:
        self._marbles[marbleIndex].position = position

    def getMarbles(self) -> List[Marble]:
        return self._marbles
    
    def getName(self) -> str:
        return self._playerName
    
    def setName(self, name: str) -> None:
        self._playerName = name


    def requestTradeCard(self) -> Card:
        """
        Lets the player choose which card he wants to give away in the traiding state at the start of each round.
        """

        if self.playedByAI:
            return self.getHandCards().pop(Random.randint(len(self.getHandCards())))
        
        else:
            print(f"---Player {self.playerName}---")
            print(f"Trade card to team mate")
            self.printHandCards()

            cardIndex = -1
            while cardIndex < 0 or cardIndex >= len(self.getHandCards()):
                cardIndex = int(print(f"[1-{len(self.getHandCards())}]")) - 1

            return self.getHandCards().pop(cardIndex)
        

    def printHandCards(self) -> None:
        """
        Prints the hand cards to the player in the console.
        """

        handCards = "- "
        for card in self.getHandCards():
            handCards += card.value[0] + " - "

        print(handCards)
    