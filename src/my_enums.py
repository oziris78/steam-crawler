
from enum import Enum


class WindowType(Enum):
    MAIN_WINDOW = 1
    SCPP = 2

    
class HandlingResult(Enum):
    GO_BACK = 1
    STAY = 2
    REFLESH = 3

