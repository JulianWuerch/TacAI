from enum import Enum


class PlayerType(Enum):
    USER = "user"
    AI = "ai"

class ActionType(Enum):
    MOVE = 0
    MOVE_BACK = 2
    EXIT = 1
    TRIX = 3
    TAC = 4
    BLOCK_NEXT = 5
    THROW = 6
    DISPOSE = 7

class CardType(Enum):
    I = ("<--1", 9)
    II = ("<--2", 7)
    III = ("<--3", 7)
    IV = ("-->4", 7)
    V = ("<--5", 7)
    VI = ("<--6", 7)
    VII = ("<--7", 8)
    VIII = ("<--8", 7)
    IX = ("<--9", 7)
    X = ("<-10", 7)
    XI = ("<-11", 0)
    XII = ("<-12", 7)
    XIII = ("<-13", 9)
    Trickster = ("Trck", 7)
    TAC = ("TAC!", 4)
    Fool = ("Fool", 0)
    Warroir = ("Warr", 0)
    Angel = ("Angl", 0)
    Devil = ("Devl", 0)


class Colors(Enum):
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    BLACK = '\033[30m'
    RESET = '\033[0m'


def match(enumType, type) -> Enum:
    """
    Matches a type to an element of an enum.

    :param enumType: The enum in which is to be searched.
    :param type: The value of the searched element.
    :return: The found enum element or None
    """
        
    for element in enumType:
        if type == element.value:
            return element

    return None
    