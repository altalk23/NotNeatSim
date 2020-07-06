from __future__ import annotations

from typing import List

from node import *
from trait import *

class Link:

    # Variable annotations
    weight: float
    inode: Node
    onode: Node

    recurrent: bool
    timeDelay: bool

    trait: Trait

    addedWeight: float

    params: List[float]

    def __init__(self,
    trait: Trait = None,
    weight: float = None,
    inode: Node = None,
    onode: Node = None,
    recurrent: bool = None,
    link: Link = None) -> None:

        # Including a trait pointer in the Link creation
        if (trait is not None and
        weight is not None and
        inode is not None and
        onode is not None and
        recurrent is not None):

            self.trait = trait
            self.weight = weight
            self.inode = inode
            self.onode = onode
            self.recurrent = recurrent

            self.addedWeight = 0
            self.timeDelay = False

        # Base Constructor
        elif (weight is not None and
        inode is not None and
        onode is not None and
        recurrent is not None):
            raise NotImplementedError

        # For when you don't know the connections yet
        elif (weight is not None):
            raise NotImplementedError

        # Copy Constructor
        elif (link is not None):
            raise NotImplementedError



    def deriveTrait(self, trait: Trait) -> None:
        raise NotImplementedError
