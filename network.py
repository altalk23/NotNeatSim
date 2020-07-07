from __future__ import annotations

from typing import List

from genome import *
from node import *
from nodetype import *

class Network:

    # Variable annotations
    linkCount: int = 0
    nodeCount: int = 0

    nodes: List[Node] = []
    inputs: List[Node] = []
    outputs: List[Node] = []

    genotype: Genome = None

    name: str = ''

    id: int = 0

    maxWeight: float = 0
    adaptable: bool = False


    def __init__(self,
    inputs: List[Node] = None,
    outputs: List[Node] = None,
    allnodes: List[Node] = None,
    id: int = None,
    adaptable: bool = None,
    network: Network = None) -> None:

        self.linkCount = -1
        self.nodeCount = -1

        # This constructor allows the input and output lists to be supplied
        if (inputs is not None and
        outputs is not None and
        allnodes is not None and
        id is not None and
        adaptable is not None):
            raise NotImplementedError

        # Same as previous but without adaptable
        elif (inputs is not None and
        outputs is not None and
        allnodes is not None and
        id is not None):

            self.inputs = inputs
            self.outputs = outputs
            self.nodes = allnodes
            self.id = id


        # This constructs a net with empty input and output lists
        elif (id is not None and
        adaptable is not None):
            raise NotImplementedError

        # Same as previous but without adaptable
        elif (id is not None):
            raise NotImplementedError

        # Copy Constructor
        elif (newtork is not None):
            raise NotImplementedError


    # Puts the network back into an inactive state
    def flush(self) -> None:
        raise NotImplementedError


    # Verify flushedness for debugging
    def verifyFlush(self) -> None:
        raise NotImplementedError


    # Activates the net such that all outputs are active
    def activate(self) -> None:
        raise NotImplementedError


    # Add a new input node
    def addInput(self, node: Node) -> None:
        raise NotImplementedError


    # Add a new output node
    def addOutput(self, node: Node) -> None:
        raise NotImplementedError


    # Loads sensor values
    def loadSensors(self, values: List[float]) -> None:
        value = iter(values)
        for input in self.inputs:
            if input.type == NodeType.SENSOR:
                input.loadSensor(next(value))



    # Takes and array of output activations and OVERRIDES the outputs' actual activations
    def overrideOutputs(self, value: float) -> None:
        raise NotImplementedError


    # Counts the number of links in the net if not yet counted
    def countLinks(self) -> int:
        raise NotImplementedError


    # This checks a POTENTIAL link if it must be recurrent
    def isRecurrent(self, inode: Node, onode: Node, count: int, threshold: int) -> bool:
        raise NotImplementedError


    # If all output are not active then return true
    def outputsOff(self) -> bool:
        raise NotImplementedError


    # Returns maximum depth:
    def maxDepth(self) -> int:
        return max(output.depth(0, self) for output in self.outputs)
