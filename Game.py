from random import Random
from typing import List
from Action import Action
from Card import Card
from Enums import CardType, PlayerType, match
from Marble import Marble
from Player import Player


class Game:
    
    PLAYER_COUNT = 4
    HAND_SIZE = 5
    MARBLE_COUNT = 4
    RING_PLACES = 64
    roundCounter: int
    players: List[Player] = []
    running: bool = False
    actionLog: List[Action] = []
    drawPile: List[Card] = []
    discardPile: List[Card] = []
    winnerTeam: str = ""
    

    def __init__(self) -> "Game":
        """
        Constructor of a game.
        """

        self.roundCounter = 0
        self.actionLog = []
        self.players = []
        for playerIndex in range(self.PLAYER_COUNT):
            name = input(f"Player {playerIndex + 1} name: ")
            type = input(f"Player {playerIndex + 1} type: ")
            print("")

            type = match(PlayerType, type)
            player = Player(playerIndex, type, name)
            playerMarbles = []
            for marbleIndex in range(self.MARBLE_COUNT):
                playerMarbles.append(Marble(marbleIndex))

            player.setMarbles(playerMarbles)
            self.players.append(player)
        
        self.drawPile = self.generateCardDeck()


    def start(self) -> List[Action]:
        """
        Starts the game.
        This function handles the whole game loop from start to finish.

        :return: The log of all actions taken in this game.
        """

        self.running = True
        while self.running:
            
            if self.needNewCards():
                self.shuffleCardDeck()

            self.dishCards()
            self.reportExitCard()
            self.tradeCards()

            for round in range(self.HAND_SIZE):
                self.playRound(round)
                self.roundCounter += 1
                self.winnerTeam = self.checkWinnCondition()

            if self.winnerTeam:
                self.celebrateTeam(self.winnerTeam)
                self.running = False
        
        return self.actionLog


    def generateCardDeck(self) -> List[Card]:
        """
        Generates and returns a full deck of cards as spezified by the counts of cards in the CardType Enum.
        :return: The new, shuffled card deck.
        """

        targetPile = []
        sourcePile = []

        for cardType in CardType:
            for _ in range(cardType.value[1]):
                sourcePile.append(Card(cardType))

        random = Random()
        while sourcePile:
            targetPile.append(sourcePile.pop(random.randint(0, len(sourcePile) - 1)))

        return targetPile
            

    def needNewCards(self) -> None:
        """
        Checks if there are enough cards left to deel a full hand to each player.
        """

        return len(self.drawPile) < self.HAND_SIZE * self.PLAYER_COUNT


    def shuffleCardDeck(self) -> None:
        """
        Shuffles all cards from the discard pile and adds them back under the draw pile.
        """
        
        newDeck = []

        random = Random()
        while self.discardPile:
            newDeck.append(self.discardPile.pop(random.randint(0, len(self.discardPile) - 1)))

        newDeck.extend(self.drawPile)
        self.drawPile = newDeck


    def dishCards(self) -> None:
        """
        This function sets the hand cards of the players with cards from the draw pile.
        """
        
        newHandCards = [[] for _ in range(self.PLAYER_COUNT)]
        for _ in range(self.HAND_SIZE):
            for handIndex in range(self.PLAYER_COUNT):
                newHandCards[handIndex].append(self.drawPile.pop())
        
        for playerIndex in range(self.PLAYER_COUNT):
            self.players[playerIndex].setHandCards(newHandCards[playerIndex])


    def reportExitCard(self) -> None:
        """
        This function sets the signalOpeningCard flag of each player. Indicating if the hand cards of the player contain a 1 or 13. 
        """
        
        for player in self.players:
            player.setSignalOpeningCard(CardType.I in player.getHandCards() or CardType.XIII in player.getHandCards())
                

    def tradeCards(self) -> None:
        """
        Lets players in a team trade one card.
        """

        givenCards = []
        for player in self.players:
            givenCards.append(player.requestTradeCard())

        for playerIndex, player in enumerate(self.players):
            player.addSingleCard(givenCards[(playerIndex + self.PLAYER_COUNT / 2) % self.PLAYER_COUNT])


    def playRound(self, round) -> None:
        """
        Executes one round. Every player choses which card to play and the actions assosiated to those cards are executed.
        
        :param round: Count of Rounds.
        """
        
        print(f"---Round {round + 1}---")

        for player in self.players:
            action = player.playCard()
            self.executeAction(action)
            self.actionLog.append(action)


    def executeAction(self, action: Action) -> None:
        pass

    def checkWinnCondition(self) -> List[int]:
        """
        Checks wherether a team has all marbles in its houses.

        :return: The indecies of the players if a team won as list.
        """

        finished = []
        for playerIndex, player in enumerate(self.players):
            playerFinished = True
            for marble in player.getMarbles():
                if marble.position < self.RING_PLACES:
                    playerFinished = False
                    break
            
            finished.append(playerFinished)
            if playerFinished and playerIndex >= self.PLAYER_COUNT / 2 and finished[playerIndex - self.PLAYER_COUNT / 2]:
                return [playerIndex - self.PLAYER_COUNT / 2, playerIndex]
            
        return False


    def celebrateTeam(self, team: List[int]):
        """
        Congratulate the players of the given team.
        :param team: The list of indecies of the players. 
        """

        print(f"---Team {team[0]} won!---")
        for playerIndex in team:
            print(f"Congratulations {self.players[playerIndex].getName()}!")
