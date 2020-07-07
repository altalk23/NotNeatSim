from __future__ import annotations

from typing import List

from node import *
from trait import *

class Link:

    # Variable annotations
    weight: float = 0
    inode: Node = None
    onode: Node = None

    recurrent: bool = False
    timeDelay: bool = False

    trait: Trait = None

    addedWeight: float = False

    params: List[float] = []

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

        # Base Constructor
        elif (weight is not None and
        inode is not None and
        onode is not None and
        recurrent is not None):

            self.weight = weight
            self.inode = inode
            self.onode = onode
            self.recurrent = recurrent

        # For when you don't know the connections yet
        elif (weight is not None):
            raise NotImplementedError

        # Copy Constructor
        elif (link is not None):
            raise NotImplementedError



    def deriveTrait(self, trait: Trait) -> None:
        self.trait = trait
