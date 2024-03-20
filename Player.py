from random import Random
from typing import List
from AI import AI
from Action import Action

from Card import Card
from Enums import PlayerType, Colors
from Marble import Marble


class Player:

    ownID: int
    playerType: PlayerType = PlayerType.USER
    playedByAI: bool = False
    ai: AI
    _playerName: str = ""
    _ownHandCards: List[Card] = []
    _signalOpeningCard: bool = False
    _marbles: List[Marble]
    _playerColor: str = ""


    def __init__(self, id: int, type: PlayerType, name: str = ""):
        """
        Constructor of a player.
        """

        self.ownID = id
        self.playerType = type
        self.playedByAI = type == PlayerType.AI
        for count, color in enumerate(Colors):
            if count == id:
                self._playerColor = color
                break

        if name:
            self._playerName = name
        else:
            self._playerName = f"Bot{id}"
            self.ai = AI()


    def playCard(self) -> Action:
        """
        Lets the player choose which card he wants to play.
        If the player is controled by an AI the AI chooses the card.

        :return: The action the player wants to take.
        """

        if self.isPlayedByAI():
            return self.ai.getAction()
        
        else:
            print(f"---Player {self.getName()}---")
            self.printHandCards()
            cardIndex = -1
            print("Play a card")

            while cardIndex < 0 or cardIndex >= len(self.getHandCards()):
                cardIndex = int(input(f"[1-{len(self.getHandCards())}]")) - 1
            
            chosenCard = self.getHandCards().pop(cardIndex)

            return chosenCard.executeCard(self.getID())


    def getID(self) -> int:
        return self.ownID
    
    def setID(self, newID) -> None:
        self.ownID = newID
    
    def getHandCards(self) -> List:
        return self._ownHandCards
    
    def setHandCards(self, newHandCards) -> None:
        self._ownHandCards = newHandCards

    def removeSingleCard(self, cardToRemove) -> None:
        self._ownHandCards.remove(cardToRemove)
    
    def getSingleCard(self, index) -> Card:
        return self._ownHandCards[index]
    
    def addSingleCard(self, cardToAdd) -> None:
        self._ownHandCards.append(cardToAdd)

    def setPlayedByAI(self, playedByAI) -> None:
        self.playedByAI = playedByAI

    def isPlayedByAI(self) -> bool:
        return self.playedByAI
    
    def setSignalOpeningCard(self, signalState: bool) -> None:
        self._signalOpeningCard = signalState

    def signalOpeningCardState(self) -> bool:
        return self._signalOpeningCard
    
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

    def getPlayerColor(self) -> str:
        return self._playerColor
    
    def setPlayerColor(self, color) -> None:
        self._playerColor = color


    def requestTradeCard(self) -> Card:
        """
        Lets the player choose which card he wants to give away in the traiding state at the start of each round.
        """
        return self.getHandCards().pop(0)
        random = Random()
        if self.playedByAI:
            return self.getHandCards().pop(random.randint(0, len(self.getHandCards())))
        
        else:
            print(f"{self.getPlayerColor().value}---Player {self._playerName}---{Colors.RESET.value}")
            print(f"{self.getPlayerColor().value}Trade card to team mate{Colors.RESET.value}")
            self.printHandCards()

            cardIndex = -1
            while cardIndex < 0 or cardIndex >= len(self.getHandCards()):
                cardIndex = int(input(f"[1-{len(self.getHandCards())}]")) - 1

            return self.getHandCards().pop(cardIndex)
        

    def printHandCards(self) -> None:
        """
        Prints the hand cards to the player in the console.
        """

        handCards = str(self.getPlayerColor().value) + "- "
        for card in self.getHandCards():
            handCards += card.type.value[0] + " - "

        handCards += str(Colors.RESET.value)

        print(handCards)
    

    def compleat(self) -> bool:
        """
        Checks if the player has all marbles in his house.
        """
        
        for marble in self.getMarbles():
            if marble.position < 65:
                return False
        
        return True