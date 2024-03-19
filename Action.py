from typing import List
from Enums import ActionType, CardType


class Action():

    type: ActionType
    actionData: List[int]
    used: bool
    playerAction: bool
    cardType: CardType
    playerID: int


    def __init__(self, type: ActionType, playerID: int, actionData: List[int] = [], cardType: CardType = None):
        self.type = type
        self.actionData = actionData
        self.used = False
        self.playerAction = False
        self.cardType = cardType
        self.playerID = playerID
