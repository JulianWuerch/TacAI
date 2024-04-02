import math
from random import Random
from typing import List
from Action import Action
from Card import Card
from Enums import ActionType, CardType, Colors, PlayerType, match
from Marble import Marble
from Player import Player


class Game:
    
    PLAYER_COUNT = 4
    HAND_SIZE = 5 # when played master-version then in every last round 6 cards
    MARBLE_COUNT = 4
    RING_PLACES = 64
    roundCounter: int
    players: List[Player] = []
    running: bool = False
    actionLog: List[Action] = []
    drawPile: List[Card] = []
    discardPile: List[Card] = []
    winnerTeam: str = ""
    printWidth = 19
    tableMarblePositions = []
    

    def __init__(self) -> "Game":
        """
        Constructor of a game.
        """

        self.roundCounter = 0
        self.actionLog = []
        self.players = []
        for playerIndex in range(self.PLAYER_COUNT):
            #name = input(f"Player {playerIndex + 1} name: ")
            #type = input(f"Player {playerIndex + 1} type: ")
            name = str(playerIndex)
            type = "player"
            print("")

            type = match(PlayerType, type)
            player = Player(playerIndex, type, name)
            playerMarbles = []
            for marbleIndex in range(self.MARBLE_COUNT):
                playerMarbles.append(Marble(marbleIndex))

            player.setMarbles(playerMarbles)
            self.players.append(player)
        
        self.drawPile = self.generateCardDeck()

        self.defineTablePositions()
        self.printGame()


    def defineTablePositions(self):
        """
        Calculates the positions of the central circle.
        """

        angle = 360 / 64
        for position in range(64):
            position = 32 - position
            x = int(self.printWidth / 2 - self.printWidth / 2 * math.sin(math.radians(angle * position)))
            y = int(self.printWidth / 2 - self.printWidth / 2 * math.cos(math.radians(angle * position)))
            x = min(max(x, 0), int(self.printWidth / 2) * 2)
            y = min(max(y, 0), int(self.printWidth / 2) * 2)
            self.tableMarblePositions.append((x, y))


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
            #self.debugCards()
            self.reportExitCard()
            self.tradeCards()

            for round in range(self.HAND_SIZE):
                self.playRound(round)
                self.roundCounter += 1

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
            player.setSignalOpeningCard(False)
            for card in player.getHandCards():
                if card.type == CardType.I or card.type == CardType.XIII:
                    player.setSignalOpeningCard(True)

            print(f"Player {player.getName()} can open?", player.signalOpeningCardState())
                

    def tradeCards(self) -> None:
        """
        Lets players in a team trade one card.
        """

        givenCards = []
        for player in self.players:
            givenCards.append(player.requestTradeCard())

        for playerIndex, player in enumerate(self.players):
            player.addSingleCard(givenCards[int((playerIndex + self.PLAYER_COUNT / 2) % self.PLAYER_COUNT)])


    def playRound(self, round) -> None:
        """
        Executes one round. Every player choses which card to play and the actions assosiated to those cards are executed.
        
        :param round: Count of Rounds.
        """
        
        print(f"---Round {round + 1}---")

        for player in self.players:
            if len(self.actionLog) > 0 and self.actionLog[-1].type == ActionType.BLOCK_NEXT:
                print("-Warning, you are blocked. Your Card will be discarded-")

            action = player.playCard()
            action.playerAction = True
            self.actionLog.append(action)
            if len(self.actionLog) == 0 or not (len(self.actionLog) == 0 or (self.actionLog[-1].type == ActionType.BLOCK_NEXT and self.actionLog[-1].used)):
                suc = self.executeAction(player, action)
                action.used = suc
            
            elif action.type == ActionType.TAC:
                if input("Use Tac to prevent block? [Y, N]").lower() == "y":
                    suc = self.executeAction(player, action)
                    action.used = suc

            self.printGame()
            for entry in self.actionLog:
                print(entry.type, entry.actionData)


            self.winnerTeam = self.checkWinnCondition((player.getID() % 2))


    def executeAction(self, player: Player, action: Action) -> bool:
        """
        Executes an action. Moves marbles and requests additional input from the player if nessecary.
        Checks if the action is possible and moves marbles acordingly.

        :param player: The player who does the action.
        :param action: The action to execute.
        :return: If the eaction was performed sucessfully.
        """

        print(player.getName(), action.type, action.actionData)
        playerID = player.getID()
        if player.compleat():
            playerID = (playerID + 2) % 4

        if action.type == ActionType.EXIT:
            for marble in self.players[playerID].getMarbles():
                if marble.position == 0:
                    position = 16 * playerID + 1
                    self.throw(position)
                    marble.position = position
                    return True
                    break

        elif action.type == ActionType.BLOCK_NEXT:
            return True

        elif action.type == ActionType.TRIX:
            pos1 = self.players[action.actionData[0][0]].getMarbles()[action.actionData[0][1]].position
            pos2 = self.players[action.actionData[1][0]].getMarbles()[action.actionData[1][1]].position

            if 0 < pos1 < 65 and 0 < pos2 < 65:

                self.players[action.actionData[0][0]].getMarbles()[action.actionData[0][1]].position = pos2
                self.players[action.actionData[1][0]].getMarbles()[action.actionData[1][1]].position = pos1

                if not self.players[action.actionData[0][0]].getMarbles()[action.actionData[0][1]].activated:
                    self.players[action.actionData[0][0]].getMarbles()[action.actionData[0][1]].trixActivated = True

                if not self.players[action.actionData[1][0]].getMarbles()[action.actionData[1][1]].activated:
                    self.players[action.actionData[1][0]].getMarbles()[action.actionData[1][1]].trixActivated = True
                
                self.players[action.actionData[0][0]].getMarbles()[action.actionData[0][1]].activated = True
                self.players[action.actionData[1][0]].getMarbles()[action.actionData[1][1]].activated = True

                return True

        elif action.type == ActionType.MOVE:
            finalPositions = []
            allSuccessfull = True
            for step in action.actionData:
                if not allSuccessfull:
                    break

                selfCompleat = True
                for marble in self.players[playerID].getMarbles():
                    if marble.position < 65:
                        willBeMoved = False
                        for targPos in finalPositions:
                            if targPos[0] == player.getID() and targPos[1] == marble.index and targPos[2] > 64:
                                willBeMoved = True

                        selfCompleat = willBeMoved
                        break

                if selfCompleat:
                    playerID = (player.getID() + 2) % 4

                marblePositions = []
                for play in self.players:
                    for marb in play.getMarbles():
                        marblePositions.append(marb.position)

                direction = 1
                if step[1] < 0:
                    direction = -1

                marble = self.players[playerID].getMarbles()[step[0]]
                startingInHouse = marble.position > 64
                if marble.position == 0 or (startingInHouse and direction < 0) or (startingInHouse and marble.position + step[1] > 68):
                    allSuccessfull = False
                    continue

                startPosition = marble.position

                if startingInHouse:
                    freePos = True
                    for i in range(1, step[1]):
                        pos = marblePositions + i
                        for marb in self.players[playerID].getMarbles():
                            if marb.position == pos:
                                freePos = False
                                allSuccessfull = False
                                break

                    if freePos:
                        finalPos = startPosition + step[1]
                        finalPositions.append([playerID, step[0], finalPos])
                        continue

                houseEntrance = playerID * 16 + 1
                i = 0
                finalPos = None
                for i in range(1, abs(step[1])):
                    pos = (startPosition + i * direction + self.RING_PLACES) % self.RING_PLACES + int((startPosition + i * direction) / self.RING_PLACES)
                    if pos == 0:
                        pos = 64
                    if pos in marblePositions:
                        allSuccessfull = False

                    if pos == houseEntrance and marble.activated:
                        housePosition = step[1] * direction - i
                        for ii in range(1, step[1] * direction - i):
                            for marb in self.players[playerID].getMarbles():
                                if marb.position == self.RING_PLACES + ii:
                                    housePosition = -1
                                    break
                        
                        if housePosition > 0 and housePosition < 5:
                            decision = input("Go in house? [Y, N]")
                            if decision.lower() == "y":
                                finalPos = self.RING_PLACES + housePosition
                                finalPositions.append([playerID, step[0], finalPos])
                                break
            
                if not finalPos:
                    finalPos = (startPosition + step[1] + self.RING_PLACES) % self.RING_PLACES + int((startPosition + i * direction) / self.RING_PLACES)
                    finalPositions.append([playerID, step[0], finalPos])

            if allSuccessfull:
                for pos in finalPositions:
                    marble = self.players[pos[0]].getMarbles()[pos[1]]
                    finalPos = pos[2]
                    self.throw(finalPos)
                    marble.position = finalPos
                    marble.activated = True
                
                return True

        elif action.type == ActionType.TAC:
            actionsToReverse = []
            lastAction = False
            for backTrackAction in reversed(self.actionLog[0:-1]):
                if backTrackAction.playerAction:
                    if lastAction:
                        break

                    else:
                        lastAction = True

                actionsToReverse.append(backTrackAction)
            
            actionsToReverse.reverse()

            actionToDo = None

            for revAction in actionsToReverse:
                if revAction.used:
                    self.reverseAction(revAction, revAction.playerID)
                    if not revAction.type == ActionType.TAC:
                        actionToDo = revAction
            

            if actionToDo is not None:
                
                playerCard = Card(actionToDo.cardType)
                playerAction = playerCard.executeCard(playerID)
                suc = self.executeAction(self.players[playerID], playerAction)
                playerAction.used = suc
                playerAction.playerAction = True

                self.actionLog.append(playerAction)
                self.printGame()

                for entry in self.actionLog:
                    print(entry.type, entry.actionData)

                return suc

    def reverseActionBlock(self, actions: List[Action]):
        pass

    
    def reverseAction(self, action: Action, playerID: int):
        """
        This function reverses actions as needed for the TAC action.

        :param action: The action that is supposed to be returned.
        :param playerID: The player who executed the action.
        """
        
        if action.type == ActionType.EXIT:
            playerGate = 16 * action.actionData + 1
            self.throw(playerGate)

        elif action.type == ActionType.BLOCK_NEXT:
            pass

        elif action.type == ActionType.THROW:
            for mar in self.players[action.actionData[0]].getMarbles():
                if mar.position == 0:
                    mar.position = action.actionData[1]
                    mar.activated = action.actionData[2]
                    self.actionLog.append(Action(ActionType.REVERSE_ACTION, playerID, [action.type, action.actionData]))
                    self.actionLog[-1].used = True
                    break

        elif action.type == ActionType.TRIX:
            pos1 = self.players[action.actionData[0][0]].getMarbles()[action.actionData[0][1]].position
            pos2 = self.players[action.actionData[1][0]].getMarbles()[action.actionData[1][1]].position

            if 0 < pos1 < 65 and 0 < pos2 < 65:

                self.players[action.actionData[0][0]].getMarbles()[action.actionData[0][1]].position = pos2
                self.players[action.actionData[1][0]].getMarbles()[action.actionData[1][1]].position = pos1

                if self.players[action.actionData[0][0]].getMarbles()[action.actionData[0][1]].trixActivated:
                    self.players[action.actionData[0][0]].getMarbles()[action.actionData[0][1]].activated = False

                if self.players[action.actionData[1][0]].getMarbles()[action.actionData[1][1]].trixActivated:
                    self.players[action.actionData[1][0]].getMarbles()[action.actionData[1][1]].activated = False

            self.actionLog.append(Action(ActionType.REVERSE_ACTION, playerID, [action.type, action.actionData]))
            self.actionLog[-1].used = True

        elif action.type == ActionType.MOVE:
            marbles = self.players[playerID].getMarbles()
            for step in action.actionData:
                position = marbles[step[0]].position
                if 0 < position < 65:
                    pos = (position + self.RING_PLACES - step[1]) % self.RING_PLACES
                    if pos == 0:
                        pos = 64

                    self.players[playerID].getMarbles()[step[0]].position = pos
                    
                elif position == 0:
                    pass

                elif position > 64:
                    if position - abs(step[1]) < 65:
                        overshoot = position - 64 - step[1]
                        houseEntry = playerID * 16 + 1
                        newPos = (houseEntry - overshoot)

                    else:
                        newPos = position - step[1]

                    self.players[playerID].getMarbles()[step[0]].position = newPos

            self.actionLog.append(Action(ActionType.REVERSE_ACTION, playerID, [action.type, action.actionData]))
            self.actionLog[-1].used = True

        elif action.type == ActionType.TAC:
            self.actionLog.append(Action(ActionType.REVERSE_ACTION, playerID, [action.type, action.actionData]))
            self.actionLog[-1].used = True
            pass

        elif action.type == ActionType.REVERSE_ACTION:
            actionToReverse = Action(action.actionData[0], action.playerID, action.actionData[1])
            suc = self.executeAction(self.players[action.playerID], actionToReverse)
            actionToReverse.used = suc
            self.actionLog.append(actionToReverse)


    def throw(self, position: int):
        """
        Throws all existing marbles at a certain position.
        If there is a marble at that position it is send to the house of its player.

        :param position: The position where to throw [1-64].
        """

        for player in self.players:
            for marble in player.getMarbles():
                if marble.position == position:
                    self.actionLog.append(Action(ActionType.THROW, player.getID(), [player.getID(), position, marble.activated]))
                    marble.position = 0
                    marble.activated = False
                    self.actionLog[-1].used = True


    def checkWinnCondition(self, playerGroup: int) -> List[int]:
        """
        Checks wherether a team has all marbles in its houses.

        :playerGroup: Which group can win at the moment.
        :return: The indecies of the players if a team won as list.
        """

        finished = []
        for playerIndex, player in enumerate(self.players):
            if (playerIndex % 2) != playerGroup:
                continue

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


    def printGame(self):
        
        for y in range(self.printWidth):
            line = ""
            for x in range(self.printWidth):
                character = "."
                if (x, y) in self.tableMarblePositions:
                    character = "O"
                
                if x == int(self.printWidth / 2):
                    if y == self.printWidth - 1:
                        character = str(self.players[0].getPlayerColor().value) + "O" + str(Colors.RESET.value)
                        
                    if y == 0:
                        character = str(self.players[2].getPlayerColor().value) + "O" + str(Colors.RESET.value)

                    for houseIndex in range(4):
                        if y == 2 + houseIndex:
                            marbleChar = "O"
                            for marble in self.players[2].getMarbles():
                                if marble.position - 65 == houseIndex:
                                    marbleChar = str(marble.index + 1)
                                    
                            character = self.players[2].getPlayerColor().value + marbleChar + Colors.RESET.value

                        if y == self.printWidth - 3 - houseIndex:
                            marbleChar = "O"
                            for marble in self.players[0].getMarbles():
                                if marble.position - 65 == houseIndex:
                                    marbleChar = str(marble.index + 1)

                            character = self.players[0].getPlayerColor().value + marbleChar + Colors.RESET.value

                
                if y == int(self.printWidth / 2):
                    if x == 0:
                        character = str(self.players[1].getPlayerColor().value) + "O" + str(Colors.RESET.value)

                    if x == self.printWidth - 1:
                        character = str(self.players[3].getPlayerColor().value) + "O" + str(Colors.RESET.value)
                        
                    for houseIndex in range(4):
                        if x == 2 + houseIndex:
                            marbleChar = "O"
                            for marble in self.players[1].getMarbles():
                                if marble.position - 65 == houseIndex:
                                    marbleChar = str(marble.index + 1)

                            character = self.players[1].getPlayerColor().value + marbleChar + Colors.RESET.value

                        if x == self.printWidth - 3 - houseIndex:
                            marbleChar = "O"
                            for marble in self.players[3].getMarbles():
                                if marble.position - 65 == houseIndex:
                                    marbleChar = str(marble.index + 1)

                            character = self.players[3].getPlayerColor().value + marbleChar + Colors.RESET.value


                for player in self.players:
                    for marble in player.getMarbles():
                        if marble.position > 0 and marble.position <= 64:
                            if self.tableMarblePositions[marble.position % self.RING_PLACES - 1] == (x, y):
                                character = str(player.getPlayerColor().value)
                                character += str(marble.index + 1)
                                character += str(Colors.RESET.value)
                                break
                
                if y == self.printWidth - 2 or y == self.printWidth - 1:
                    if x == self.printWidth - 2 or x == self.printWidth - 1:
                        if self.players[0].getMarbles()[(x - self.printWidth + 2) + (y - self.printWidth + 2) * 2].position == 0:
                            character = str(self.players[0].getPlayerColor().value) + f"{(x - self.printWidth + 2) + (y - self.printWidth + 2) * 2 + 1}" + str(Colors.RESET.value)
                
                if y == self.printWidth - 2 or y == self.printWidth - 1:
                    if x == 0 or x == 1:
                        if self.players[1].getMarbles()[x + (y - self.printWidth + 2) * 2].position == 0:
                            character = str(self.players[1].getPlayerColor().value) + f"{x + (y - self.printWidth + 2) * 2 + 1}" + str(Colors.RESET.value)

                if y == 0 or y == 1:
                    if x == 0 or x == 1:
                        if self.players[2].getMarbles()[x + y * 2].position == 0:
                            character = str(self.players[2].getPlayerColor().value) + f"{x + y * 2 + 1}" + str(Colors.RESET.value)

                if y == 0 or y == 1:
                    if x == self.printWidth - 2 or x == self.printWidth - 1:
                        if self.players[3].getMarbles()[(x - self.printWidth + 2) + y * 2].position == 0:
                            character = str(self.players[3].getPlayerColor().value) + f"{(x - self.printWidth + 2) + y * 2 + 1}" + str(Colors.RESET.value)

                line += character + " "
            
            print(line)


    def debugCards(self):
        """
        A debug function to set cards of the players to ensure certain card combinations.
        """

        for player in self.players:
            newCards = [Card(CardType.V), Card(CardType.I), Card(CardType.IV), Card(CardType.TAC), Card(CardType.Trickster)]
            player.setHandCards(newCards)