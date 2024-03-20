from Action import Action
from Enums import ActionType, CardType, Colors


class Card:

    type: CardType = CardType.XI

    def __init__(self, type: CardType) -> "Card":
        self.type = type

    
    def executeCard(self, playerID: int) -> Action:
        """
        Only for humans.
        Executes the card for the user and requests all addidtional information the card needs.

        :param playerID: The id of the executing player.
        """
        
        if self.type == CardType.I:
            choice = input("Exit or move? [E, M]").upper()
            if choice == "E":
                return Action(ActionType.EXIT, playerID, playerID, cardType=CardType.I)
            else:
                marble = int(input("Which marble do you want to move? [1-4]")) - 1
                return Action(ActionType.MOVE, playerID, [(marble, 1)], cardType=CardType.I)
        elif self.type == CardType.II:
            marble = int(input("Which marble do you want to move? [1-4]")) - 1
            return Action(ActionType.MOVE, playerID, [(marble, 2)], cardType=CardType.II)
        elif self.type == CardType.III:
            marble = int(input("Which marble do you want to move? [1-4]")) - 1
            return Action(ActionType.MOVE, playerID, [(marble, 3)], cardType=CardType.III)
        elif self.type == CardType.IV:
            marble = int(input("Which marble do you want to move? [1-4]")) - 1
            return Action(ActionType.MOVE, playerID, [(marble, -4)], cardType=CardType.IV)
        elif self.type == CardType.V:
            marble = int(input("Which marble do you want to move? [1-4]")) - 1
            return Action(ActionType.MOVE, playerID, [(marble, 5)], cardType=CardType.V)
        elif self.type == CardType.VI:
            marble = int(input("Which marble do you want to move? [1-4]")) - 1
            return Action(ActionType.MOVE, playerID, [(marble, 6)], cardType=CardType.VI)
        elif self.type == CardType.VII:
            freeSteps = 7
            moves = []
            while freeSteps > 0:
                marble = int(input("Which marble do you want to move? [1-4]")) - 1
                steps = int(input(f"How manny steps? {freeSteps} "))
                for _ in range(steps):
                    moves.append((marble, 1))
                    
                freeSteps -= abs(steps)
            return Action(ActionType.MOVE, playerID, moves, cardType=CardType.VII)
        elif self.type == CardType.VIII:
            choice = input("Block next Player or move? [B, M]").upper()
            if choice == "B":
                return Action(ActionType.BLOCK_NEXT, playerID, cardType=CardType.VIII)
            else:
                marble = int(input("Which marble do you want to move? [1-4]")) - 1
                return Action(ActionType.MOVE, playerID, [(marble, 8)], cardType=CardType.VIII)
        elif self.type == CardType.IX:
            marble = int(input("Which marble do you want to move? [1-4]")) - 1
            return Action(ActionType.MOVE, playerID, [(marble, 9)], cardType=CardType.IX)
        elif self.type == CardType.X:
            marble = int(input("Which marble do you want to move? [1-4]")) - 1
            return Action(ActionType.MOVE, playerID, [(marble, 10)], cardType=CardType.X)
        elif self.type == CardType.XI:
            marble = int(input("Which marble do you want to move? [1-4]")) - 1
            return Action(ActionType.MOVE, playerID, [(marble, 11)], cardType=CardType.XI)
        elif self.type == CardType.XII:
            marble = int(input("Which marble do you want to move? [1-4]")) - 1
            return Action(ActionType.MOVE, playerID, [(marble, 12)], cardType=CardType.XII)
        elif self.type == CardType.XIII:
            choice = input("Exit or move? [E, M]").upper()
            if choice == "E":
                return Action(ActionType.EXIT, playerID, cardType=CardType.XIII)
            
            else:
                marble = int(input("Which marble do you want to move? [1-4]")) - 1
                return Action(ActionType.MOVE, playerID, [(marble, 13)], cardType=CardType.XIII)
            
        elif self.type == CardType.Trickster:
            playerString = ""
            for playerIndex, playerColor in enumerate(Colors):
                if playerIndex == 4:
                    break

                playerString += str(playerColor.value) + str(playerIndex + 1) + str(Colors.RESET.value)

            playerSource = int(input(f"Player1? [1-4] {playerString} ")) - 1
            marbleSource = int(input("Which marble do you want to move? [1-4]")) - 1
            playerTarget = int(input(f"Player2? [1-4] {playerString} ")) - 1
            marbleTarget = int(input("Which marble do you want to move? [1-4]")) - 1
            return Action(ActionType.TRIX, playerID, [(playerSource, marbleSource), (playerTarget, marbleTarget)], cardType=CardType.Trickster)
        elif self.type == CardType.TAC:
            return Action(ActionType.TAC, playerID, [], cardType=CardType.TAC)
        elif self.type == CardType.Fool:
            pass
        elif self.type == CardType.Warroir:
            pass
        elif self.type == CardType.Angel:
            pass
        elif self.type == CardType.Devil:
            pass
