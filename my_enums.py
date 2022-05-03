
from enum import Enum



class WindowType(Enum):
    TELEK_PY_HUB = 1
    SCPP = 2

    
class HandlingResult(Enum):
    GO_BACK = 1
    STAY = 2
    REFLESH = 3