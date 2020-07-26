from __future__ import annotations

from typing import Dict, List, TextIO

from link import *
from node import *
from trait import *

class Gene:

    # Variable annotations
    link: Link
    innovation: float
    mutation: float
    enable: bool
    frozen: bool

    def __init__(self,
        gene: Gene = None,
        trait: Trait = None,
        weight: float = None,
        inode: Node = None,
        onode: Node = None,
        recurrent: bool = None,
        innovation: float = None,
        mutation: int = None,
        file: TextIO = None,
        traits: List[Trait] = None,
        nodes: List[Node] = None,
        data: Dict[str, object] = None) -> None:

        self.link = Link()

        # Construct a gene with a trait
        if (trait is not None and
        weight is not None and
        inode is not None and
        onode is not None and
        recurrent is not None and
        innovation is not None and
        mutation is not None):

            self.enable = True
            self.frozen = False

            self.link = Link(trait=trait, weight=weight, inode=inode, onode=onode, recurrent=recurrent)
            self.innovation = innovation
            self.mutation = mutation

        # Construct a gene with no trait
        elif (weight is not None and
        inode is not None and
        onode is not None and
        recurrent is not None and
        innovation is not None and
        mutation is not None):
            raise NotImplementedError

        # Construct a gene off of another gene as a duplicate
        elif (gene is not None and
        trait is not None and
        inode is not None and
        onode is not None):

            self.link = Link(trait=trait, weight=gene.link.weight, inode=inode, onode=onode, recurrent=gene.link.recurrent)
            self.innovation = gene.innovation
            self.mutation = gene.mutation
            self.enable = gene.enable
            self.frozen = gene.frozen

        # Construct a gene from a file spec given traits and nodes
        elif (data is not None and
        traits is not None and
        nodes is not None):

            inode: Node
            onode: Node
            trait: Trait

            self.frozen = False

            self.innovation = data['innovation']
            self.mutation = data['mutation']
            self.enable = data['enable']

            if data['trait'] == 0:
                trait = None
            else:
                for trait in traits:
                    if trait.id == data['trait']:
                        self.trait = trait
                        break

            for node in nodes:
                if node.id == data['input']:
                    inode = node
                if node.id == data['output']:
                    onode = node

            self.link = Link(trait=trait, weight=data['weight'], inode=inode, onode=onode, recurrent=data['recurrent'])


    # Return the dict representation of the object
    def toDict(self) -> Dict[str, object]:
        data = {}

        data['trait'] = self.link.trait.id
        data['input'] = self.link.inode.id
        data['output'] = self.link.onode.id
        data['weight'] = self.link.weight
        data['recurrent'] = self.link.recurrent
        data['innovation'] = self.innovation
        data['mutation'] = self.mutation
        data['enable'] = self.enable

        return data
