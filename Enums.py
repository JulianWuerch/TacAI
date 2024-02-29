from enum import Enum


class PlayerType(Enum):
    USER = "user"
    AI = "ai"

class ActionType(Enum):
    PLAY_CARD = 0

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
    Fool = ("Fool", 1)
    Warroir = ("Warr", 1)
    Angel = ("Angl", 1)
    Devil = ("Devl", 1)


def match(enumType, type) -> Enum:
    """
    Matches a type to an element of an enum.

    :param enumType: The enum in which is to be searched.
    :param type: The value of the searched element.
    :return: The found enum element or None
    """
        
    for element in enumType:
        if type == element.value():
            return element

    return None
    