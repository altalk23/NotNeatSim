from __future__ import annotations

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

    recurrent: bool


    def __init__(self,
    inode: int = None,
    onode: int = None,
    num1: float = None,
    num2: float = None,
    newNode: int = None,
    oldNum: float = None,
    weight: float = None,
    trait: int = None,
    recurrent: bool = False) -> None:

        # Constructor for the new node case
        if (inode is not None and
        onode is not None and
        num1 is not None and
        num2 is not None and
        newNode is not None and
        oldNum is not None):
            self.type = InnovationType.NEWNODE
            self.newWeight = None
            self.newTrait = None
            self.recurrent = None

            self.inode = inode
            self.onode = onode
            self.num1 = num1
            self.num2 = num2
            self.newNode = newNode
            self.oldNum = oldNum

        # Constructor for new link case
        elif (inode is not None and
        onode is not None and
        num1 is not None and
        weight is not None and
        trait is not None):
            self.type = InnovationType.NEWLINK
            self.num2 = None
            self.newNode = None

            self.inode = inode
            self.onode = onode
            self.num1 = num1
            self.weight = weight
            self.trait = trait
            self.recurrent = recurrent
