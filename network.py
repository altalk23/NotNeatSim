from __future__ import annotations

from typing import List

from genome import *
from node import *
from nodetype import *
from print import *

class Network:

    # Variable annotations
    linkCount: int = 0
    nodeCount: int = 0

    nodes: List[Node]
    inputs: List[Node]
    outputs: List[Node]

    genotype: Genome = None

    name: str = ''

    id: int = 0

    maxWeight: float = 0
    adaptable: bool = False

    outputList: List[float]


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

        for output in self.outputs:
            output.flushback()



    # Verify flushedness for debugging
    def verifyFlush(self) -> None:
        raise NotImplementedError


    # Activates the net such that all outputs are active
    def activate(self) -> bool:

        oneTime = False

        # Keep activating until all the outputs have become active
        if self.outputsOff():



            # For each node, compute the aggregation of its incoming activation
            for node in self.nodes:

                # Ignore SENSORS
                if node.type is not NodeType.SENSOR:

                    node.inputs = []
                    node.activeFlag = False

                    # For each incoming connection, add the activity from the connection to the activesum
                    for link in node.incoming:
                        # Handle possible time delays
                        if not link.timeDelay:
                            node.inputs.append(link.weight * link.inode.getActiveOut())

                            if (link.inode.activeFlag or link.inode.type is NodeType.SENSOR):
                                node.activeFlag = True

                        # Input over a time delayed connection
                        else:
                            node.inputs.append(link.weight * link.inode.getActiveOutPrevious())

            # Now activate all the non-sensor nodes off their incoming activation
            for node in self.nodes:

                # Only activate if some active input came in
                if node.type is not NodeType.SENSOR and node.activeFlag:

                    # Keep a memory of activations for potential time delayed connections
                    node.lastActivation2 = node.lastActivation
                    node.lastActivation = node.output

                    # If the node is being overrided from outside, stick in the override value
                    if node.override:
                        node.outputOverride()

                    # Now run the net activation through an activation function
                    else:
                        node.output = node.activation(node.aggregation(node.inputs))

                    # Increment the activationCount

                    node.activationCount += 1

        if self.adaptable:
            # ADAPTATION:  Adapt weights based on activations
            for node in self.nodes:
                if node.type is not NodeType.SENSOR:
                    # For each incoming connection, perform adaptation based on the trait of the connection
                    for link in node.incoming:
                        if link.trait.id == 2 or link.trait.id == 3 or link.trait.id == 4:
                            # In the recurrent case we must take the last activation of the input for calculating hebbian changes
                            if link.recurrent:
                                link.weight = neat.hebbian(link.weight,
                                self.maxWeight,
                                link.inode.lastActivation,
                                link.onode.getActiveOut(),
                                link.params[0:3])
                            else:
                                link.weight = neat.hebbian(link.weight,
                                self.maxWeight,
                                link.inode.getActiveOut(),
                                link.onode.getActiveOut(),
                                link.params[0:3])
        return True



    # Add a new input node
    def addInput(self, node: Node) -> None:
        raise NotImplementedError


    # Add a new output node
    def addOutput(self, node: Node) -> None:
        raise NotImplementedError


    # Loads sensor values
    def loadSensors(self, values: List[float]) -> None:
        for input, value in zip(self.inputs, values):
            if input.type == NodeType.SENSOR:
                input.loadSensor(value)


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
        for node in self.outputs:
            if node.activationCount == 0:
                return True
        return False


    # Returns maximum depth:
    def maxDepth(self) -> int:
        return max(output.depth(0, self) for output in self.outputs)
