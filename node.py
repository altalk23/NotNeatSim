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
import neat

class Node:

    # Variable annotations
    activationCount: int = 0
    lastActivation: float = 0
    lastActivation2: float = 0

    trait: Trait = None

    duplicate: Node = None
    analogue: Node = None

    override: float = 0

    frozen: bool = False

    type: NodeType = None
    place: NodePlace = None
    activation: Callable = None
    aggregation: Callable = None

    input: List[float] = []
    output: float = 0

    incoming: List[Link] = []
    outcoming: List[Link] = []

    rowLevels: List[float] = []
    row: int
    xpos: int
    ypos: int

    id: int = 0

    activeFlag: bool = False


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

            self.type = type
            self.id = id

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
        return max(self.output, 0)


    # Return activation from PREVIOUS time step
    def getActiveOutPrevious(self) -> float:
        raise NotImplementedError


    # If the node is a SENSOR, returns true and loads the value
    def loadSensor(self, value: float) -> None:
        if self.type == NodeType.SENSOR:
            self.activationCount += 1
            self.lastActivation2 = self.lastActivation
            self.lastActivation = self.output
            self.output = value



    # Adds a Link to a new node in the incoming list
    def addIncoming(self, weight: float, recurrent: bool = False):
        raise NotImplementedError


    # Recursively deactivate backwards through the network
    def flushback(self) -> None:

        # A sensor should not flush black
        if self.type != NodeType.SENSOR:
            if self.activationCount > 0:
                self.activationCount = 0
                self.output = 0
                self.lastActivation = 0
                self.lastActivation2 = 0

            # Flush back recursively
            for link in self.incoming:
                # Flush the link itself (For future learning parameters possibility)
                link.addedWeight = 0
                if link.inode.activationCount > 0:
                    link.inode.flushback()
        else:
            # Flush the SENSOR
            self.activationCount = 0
            self.output = 0
            self.lastActivation = 0
            self.lastActivation2 = 0
        


    # Have node gain its properties from the trait
    def deriveTrait(self, trait: Trait) -> None:
        self.trait = trait


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
        # Noice
        if depth > 30:
            return 10

        # Base case
        if self.type == NodeType.SENSOR:
            return depth

        else:
            return max(link.inode.depth(depth + 1, network) for link in self.incoming)
