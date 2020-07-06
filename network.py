from __future__ import annotations

from typing import List

from genome import Genome
from node import Node

class Network:

    # Variable annotations
    linkCount: int

    nodes: List[Node]
    inputs: List[Node]
    outputs: List[Node]

    genotype: Genome

    name: str

    id: int

    maxWeight: float
    adaptable: bool


    def __init__(self,
    in: List[Node],
    out: List[Node],
    all: List[Node],
    id: int,
    adaptable: bool,
    network: Network) -> None:

        # This constructor allows the input and output lists to be supplied
        if (in is not None and
        out is not None and
        all is not None and
        id is not None and
        adaptable is not None):
            raise NotImplementedError

        # Same as previous but without adaptable
        elif (in is not None and
        out is not None and
        all is not None and
        id is not None):
            raise NotImplementedError

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


    # Loads sensor calues
    def loadSensors(self, value: float = None, values: List[float] = None) -> None:
        raise NotImplementedError


    # Takes and array of output activations and OVERRIDES the outputs' actual activations
    def overrideOutputs(self, value: float) -> None:
        raise NotImplementedError


    # Counts the number of links in the net if not yet counted
    def countLinks(self) -> int:
        raise NotImplementedError


    # This checks a POTENTIAL link if it must be recurrent
    def isRecurrent(self, in: Node, out: Node, count: int, threshold: int) -> bool:
        raise NotImplementedError


    # If all output are not active then return true
    def outputsOff(self) -> bool:
        raise NotImplementedError


    # Returns maximum depth:
    def maxDepth(self) -> int:
        raise NotImplementedError
