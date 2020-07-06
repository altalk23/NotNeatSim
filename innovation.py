from enum import Enum

class InnovationType(Enum):
    NEWNODE = 0
	NEWLINK = 1

class Innovation:

    # Variable annotations
    type: InnovationType

    inode: int
    onode: int

    num1: float
    num2: float

    newWeight: float
    newTrait: int
    newNode: int

    oldNum: float

    recur: bool


    def __init__(self,
    inode: int = None,
    onode: int = None,
    num1: float = None,
    num2: float = None,
    newNode: int = None,
    oldNum: float = None,
    weight: float = None,
    trait: int = None,
    recur: bool = None) -> None:

        # Constructor for the new node case
        if (inode is not None and
        onode is not None and
        num1 is not None and
        num2 is not None and
        newNode is not None and
        oldNum is not None):
            raise NotImplementedError

        # Constructor for a recur link
        elif (inode is not None and
        onode is not None and
        num1 is not None and
        weight is not None and
        trait is not None and
        recur is not None):
            raise NotImplementedError

        # Constructor for new link case
        elif (inode is not None and
        onode is not None and
        num1 is not None and
        weight is not None and
        trait is not None):
            raise NotImplementedError
