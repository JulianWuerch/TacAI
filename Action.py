from typing import List
from Enums import ActionType


class Action():

    type: ActionType
    actionData: List[int]
    used: bool
    playerAction: bool


    def __init__(self, type: ActionType, actionData: List[int] = []):
        self.type = type
        self.actionData = actionData
        self.used = False
        self.playerAction = False