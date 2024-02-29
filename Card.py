from Action import Action
from Enums import CardType


class Card:

    type: CardType = CardType.XI

    def __init__(self, type: CardType) -> "Card":
        self.type = type

    
    def executeCard(self) -> Action:
        """
        Only for humans.
        Executes the card for the user and requests all addidtional information the card needs.
        """

        pass
