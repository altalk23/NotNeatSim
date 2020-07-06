from __future__ import annotations

from math import isnan
from typing import Callable, Dict, List

from activation import *
from aggregation import *
from link import *
from network import *
from nodeplace import *
from nodetype import *
from trait import *

class Node:

    # Variable annotations
    activationCount: int
    lastActivation: float
    lastActivation2: float

    trait: Trait

    duplicate: Node
    analogue: Node

    override: float

    frozen: bool

    type: NodeType
    place: NodePlace
    activation: Callable
    aggregation: Callable

    input: List[float]
    output: float

    incoming: List[Link]
    outcoming: List[Link]

    rowLevels: List[float]
    row: int
    xpos: int
    ypos: int

    id: int


    def __init__(self,
    type: NodeType = None,
    id: int = None,
    place: NodePlace = None,
    node: Node = None,
    trait: Trait = None,
    traits: List[Trait] = None,
    data: Dict = None) -> None:

        # Construct a node from type, id and place
        if (type is not None and
        id is not None and
        place is not None):
            raise NotImplementedError

        # Construct a node from type and id
        elif (type is not None and
        id is not None):
            raise NotImplementedError

        # Construct a node off another node for genome purposes
        elif (node is not None and
        trait is not None):
            raise NotImplementedError

        # Generate the object from dict
        elif (data is not None and
        traits is not None):
        
            self.frozen = False
            self.override = float('nan')

            self.id = data['id']
            self.type = NodeType(data['type'])
            self.place = NodePlace(data['place'])

            if data['trait'] == 0:
                self.trait = None
            else:
                for trait in traits:
                    if trait.id == data['trait']:
                        self.trait = trait
                        break


    # Return the dict representation of the object
    def toDict(self) -> Dict[str, object]:
        raise NotImplementedError


    # Just return activation for step
    def getActiveOut(self) -> float:
        raise NotImplementedError


    # Return activation from PREVIOUS time step
    def getActiveOutPrevious(self) -> float:
        raise NotImplementedError


    # If the node is a SENSOR, returns true and loads the value
    def loadSensor(self, value: float) -> None:
        raise NotImplementedError


    # Adds a Link to a new node in the incoming list
    def addIncoming(self, weight: float, recurrent: bool = False):
        raise NotImplementedError


    # Recursively deactivate backwards through the network
    def flushback(self) -> None:
        raise NotImplementedError


    # Have node gain its properties from the trait
    def deriveTrait(self, trait: Trait) -> None:
        raise NotImplementedError


    # Set activation to the override value and turn off override
    def outputOverride(self) -> None:
        if not isnan(self.override):
            self.output = self.override
            self.override = float('nan')


    # Writes back changes weight values into the genome
    def lamarck(self) -> None:
        raise NotImplementedError


    # Find the greatest depth starting from this neuron at depth
    def depth(self, depth: int, network: Network) -> int:
        raise NotImplementedError
