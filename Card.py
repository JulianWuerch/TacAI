from Action import Action
from Enums import ActionType, CardType, Colors


class Card:

    type: CardType = CardType.XI

    def __init__(self, type: CardType) -> "Card":
        self.type = type

    
    def executeCard(self) -> Action:
        """
        Only for humans.
        Executes the card for the user and requests all addidtional information the card needs.
        """

        if self.type == CardType.I:
            choice = input("Exit or move? [E, M]").upper()
            if choice == "E":
                return Action(ActionType.EXIT)
            else:
                marble = int(input("Which marble do you want to move?")) - 1
                return Action(ActionType.MOVE, [(marble, 1)])
        elif self.type == CardType.II:
            marble = int(input("Which marble do you want to move?")) - 1
            return Action(ActionType.MOVE, [(marble, 2)])
        elif self.type == CardType.III:
            marble = int(input("Which marble do you want to move?")) - 1
            return Action(ActionType.MOVE, [(marble, 3)])
        elif self.type == CardType.IV:
            marble = int(input("Which marble do you want to move?")) - 1
            return Action(ActionType.MOVE, [(marble, -4)])
        elif self.type == CardType.V:
            marble = int(input("Which marble do you want to move?")) - 1
            return Action(ActionType.MOVE, [(marble, 5)])
        elif self.type == CardType.VI:
            marble = int(input("Which marble do you want to move?")) - 1
            return Action(ActionType.MOVE, [(marble, 6)])
        elif self.type == CardType.VII:
            freeSteps = 7
            moves = []
            while freeSteps > 0:
                marble = int(input("Which marble do you want to move?")) - 1
                steps = int(input(f"How manny steps? {freeSteps} "))
                for _ in range(steps):
                    moves.append((marble, 1))
                    
                freeSteps -= abs(steps)
            return Action(ActionType.MOVE, moves)
        elif self.type == CardType.VIII:
            choice = input("Block next Player or move? [B, M]").upper()
            if choice == "B":
                return Action(ActionType.BLOCK_NEXT)
            else:
                marble = int(input("Which marble do you want to move?")) - 1
                return Action(ActionType.MOVE, [(marble, 8)])
        elif self.type == CardType.IX:
            marble = int(input("Which marble do you want to move?")) - 1
            return Action(ActionType.MOVE, [(marble, 9)])
        elif self.type == CardType.X:
            marble = int(input("Which marble do you want to move?")) - 1
            return Action(ActionType.MOVE, [(marble, 10)])
        elif self.type == CardType.XI:
            marble = int(input("Which marble do you want to move?")) - 1
            return Action(ActionType.MOVE, [(marble, 11)])
        elif self.type == CardType.XII:
            marble = int(input("Which marble do you want to move?")) - 1
            return Action(ActionType.MOVE, [(marble, 12)])
        elif self.type == CardType.XIII:
            choice = input("Exit or move? [E, M]").upper()
            if choice == "E":
                return Action(ActionType.EXIT)
            
            else:
                marble = int(input("Which marble do you want to move?")) - 1
                return Action(ActionType.MOVE, [(marble, 13)])
            
        elif self.type == CardType.Trickster:
            playerString = ""
            for playerIndex, playerColor in enumerate(Colors):
                if playerIndex == 4:
                    break

                playerString += str(playerColor.value) + str(playerIndex + 1) + str(Colors.RESET.value)

            playerSource = int(input(f"Player1? [1-4] {playerString} ")) - 1
            marbleSource = int(input("Which marble do you want to move? ")) - 1
            playerTarget = int(input(f"Player2? [1-4] {playerString} ")) - 1
            marbleTarget = int(input("Which marble do you want to move? ")) - 1
            return Action(ActionType.TRIX, [(playerSource, marbleSource), (playerTarget, marbleTarget)])
        elif self.type == CardType.TAC:
            return Action(ActionType.TAC, [])
        elif self.type == CardType.Fool:
            pass
        elif self.type == CardType.Warroir:
            pass
        elif self.type == CardType.Angel:
            pass
        elif self.type == CardType.Devil:
            pass
