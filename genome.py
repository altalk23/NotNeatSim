from __future__ import annotations

from copy import deepcopy
from random import choice, random, uniform
from typing import Dict, List

from gene import *
from mutator import *
from network import *
from node import *
from nodeplace import *
from trait import *
import neat

class Genome:

    # Variable annotations
    id: int

    traits: List[Trait] = []
    genes: List[Gene] = []
    nodes: List[Node] = []

    phenotype: Network


    def __init__(self,
    id: int = None,
    traits: List[Trait] = None,
    genes: List[Gene] = None,
    nodes: List[Node] = None,
    links: List[Link] = None,
    inum: int = None,
    hnum: int = None,
    onum: int = None,
    hmax: int = None,
    recurrent: bool = None,
    linkProbability: float = None,
    type: int = None,
    data: Dict[str, object] = None) -> None:

        # This special constructor creates a Genome...
        if (id is not None and
        inum is not None and
        hnum is not None and
        onum is not None and
        hmax is not None and
        recurrent is not None and
        linkProbability is not None):
            raise NotImplementedError

        # Special constructor that creates a Genome of 3 possible types
        elif (type is not None and
        inum is not None and
        hnum is not None and
        onum is not None):
            raise NotImplementedError

        # Constructor which takes full genome specs and puts them into the new one
        elif (id is not None and
        traits is not None and
        nodes is not None and
        genes is not None):
            raise NotImplementedError

        # Constructor which takes in links (not genes) and creates a Genome
        elif (id is not None and
        traits is not None and
        nodes is not None and
        links is not None):
            raise NotImplementedError

        # Generate the object from dict
        elif (data is not None):
            self.id = data['id']

            self.traits = [Trait(data=d) for d in data['traits']]
            self.nodes = [Node(data=d, traits=self.traits) for d in data['nodes']]
            self.genes = [Gene(data=d, traits=self.traits, nodes=self.nodes) for d in data['genes']]


    # Loads a new Genome from a file
    def newGenomeLoad(self, filename: str) -> Genome:
        raise NotImplementedError


    # Generate a network phenotype from this Genome with specified id
    def genesis(self, id: int) -> Newtork:

        inputList: List[Node] = []
        outputList: List[Node] = []
        allList: List[Node] = []

        inode: Node
        onode: Node

        newNode: Node
        newLink: Link
        newNet: Network

        maxWeight: float = 0

        # Create the nodes
        for node in self.nodes:
            newNode = Node(type=node.type, id=node.id)

            newNode.deriveTrait(node.trait)

            # Check for input or output designation of node
            if node.place is NodePlace.INPUT:
                inputList.append(newNode)
            elif node.place is NodePlace.BIAS:
                inputList.append(newNode)
            elif node.place is NodePlace.OUTPUT:
                outputList.append(newNode)

            # Keep track of all nodes, not just input and output
            allList.append(newNode)

            # Have the node specifier point to the node it generated
            node.analogue = newNode

        # Create the links by iterating through the genes
        for gene in self.genes:
            # Only create the link if the gene is enabled
            if gene.enable:
                inode = gene.link.inode.analogue
                onode = gene.link.onode.analogue

                # NOTE: This line could be run through a recurrency check if desired
                newLink = Link(weight=gene.link.weight, inode=inode, onode=onode, recurrent=gene.link.recurrent)

                onode.incoming.append(newLink)
                inode.outcoming.append(newLink)

                # Derive link's parameters from its Trait pointer
                newLink.deriveTrait(gene.link.trait)

                # Keep track of maximum weight
                maxWeight = max(maxWeight, abs(newLink.weight))

        # Create the new network
        newNet = Network(inputs=inputList, outputs=outputList, allnodes=allList, id=id)

        # Attach genotype and phenotype together
        newNet.genotype = self
        self.phenotype = newNet

        newNet.maxWeight = maxWeight

        return newNet




    # For debugging: A number of tests can be run on a genome to check its integrity
    def verify(self) -> bool:
        raise NotImplementedError


    # Dump this genome to specified file
    def printToFile(self, filename: str) -> None:
        raise NotImplementedError


    # Dump this genome to a dict object
    def toDict(self) -> Dict[str, object]:
        data = {}

        data['id'] = self.id

        data['traits'] = self.traits
        data['genes'] = self.genes
        data['nodes'] = self.nodes


    # Duplicate this Genome to create a new one with the specified id
    def duplicate(self, id: int) -> Genome:
        genome = deepcopy(self)
        genome.id = id
        return genome


    # Return id of final Node in Genome
    def getLastNodeId(self) -> int:
        return self.nodes[-1].id + 1


    # Return last innovation number in Genome
    def getLastInnovationNumber(self) -> double:
        return self.genes[-1].innovation + 1


    # Perturb params in one trait
    def mutateRandomTrait(self) -> None:
        raise NotImplementedError


    # Change random link's trait. Repeat count times
    def mutateLinkTrait(self, count: int) -> None:
        raise NotImplementedError


    # Change random node's trait count times
    def mutateNodeTrait(self, count: int) -> None:
        raise NotImplementedError


    # Add Gaussian noise to linkweights either GAUSSIAN or UNIFORM (from zero)
    def mutateLinkWeights(self, power: float, rate: float, mutationType: Mutator) -> None:

        # Once in a while really shake things up
        severe: bool = False

        if random() > 0.5:
            severe = True

        num = 0
        # Loop on all genes
        for gene in self.genes:
            # Don't mutate weights of frozen links
            if not gene.frozen:

                # For severe ones
                if severe:
                    gausspoint = 0.7
                    coldgausspoint = 0.2

                # For last genes
                elif len(self.genes) >= 10 and num > len(self.genes) * 0.8:
                    gausspoint = 0.5
                    coldgausspoint = 0.2

                else:
                    # Half the time don't do any cold mutations
                    if random() > 0.5:
                        gausspoint = rate
                        coldgausspoint = 0.1
                    else:
                        gausspoint = rate
                        coldgausspoint = 0

                randnum = uniform(-1, 1) * power

                if mutationType is Mutator.GAUSSIAN:
                    if random() > gausspoint:
                        gene.link.weight += randnum
                    elif random() > coldgausspoint:
                        gene.link.weight = randnum
                elif mutationType is Mutator.COLDGAUSSIAN:
                    gene.link.weight = randnum

                gene.link.weight = min(max(gene.link.weight, -8), 8)

                gene.mutation = gene.link.weight

                num += 1




    # Toggle genes on or off
    def mutateToggleEnable(self, count: int) -> None:
        raise NotImplementedError


    # Find first disabled gene and enable it
    def mutateGeneReenable(self) -> None:
        raise NotImplementedError


    # Mutate genome by adding a node respresentation
    def mutateAddNode(self, innovations: List[Innovation], currentInnovationNumber: int, currentNodeId: int) -> None:
        raise NotImplementedError

    """
    CODED BY BIRKIY
    fixed
    """
    # Mutate the genome by adding a new link between 2 random nodes
    def mutateAddLink(self, innovations: List[Innovation], currentInnovationNumber: int, tries: int) -> None:
        nodeCount: int # Counter for finding nodes
        node1: Node # Pointers to the nodes
        node2: Node # Pointers to the nodes
        found: bool = False # Tells whether an open pair was found

        isRecurrent: bool # Indicates whether proposed link is recurrent
        newGene: Gene # The new gene

        trait: Trait # Random trait finder

        newWeight: float # The new weight for the new link

        done: bool
        recurrent: bool = False
        loopRecurrent: bool
        firstNonSensorIndex: int = 0

        # These are used to avoid getting stuck in an infinite loop checking
    	# for recursion
        # Note that we check for recursion to control the frequency of
    	# adding recurrent links rather than to prevent any paricular
    	# kind of error

        thresh: int = len(self.nodes)**2
        count: int = 0

        # Make attempts to find an unconnected pair
        tryCount = 0

        # Decide whether to make this recurrent
        if random() < neat.recurrentOnlyProbability:
            recurrent = True

        # Find the first non-sensor so that the to-node won't look at sensors as
    	# possible destinations
        firstNonSensorIndex = 0
        for index, node in enumerate(self.nodes):
            if node.type is not NodeType.SENSOR:
                firstNonSensorIndex = index
                break

        # Here is the recurrent finder loop- it is done separately
        if recurrent:
            while tryCount < tries:
                # Some of the time try to make a recur loop
                if random() > 0.5:
                    loopRecurrent = True
                else:
                    loopRecurrent = False

                if loopRecurrent:
                    node1 = choice(self.nodes[firstNonSensorIndex:])
                    node2 = node1
                else:
                    # Choose random node
                    node1 = choice(self.nodes)
                    node2 = choice(self.nodes[firstNonSensorIndex:])


                # See if a recurrent link already exists  ALSO STOP AT END OF GENES!!!!
                for gene in self.genes:

                    if not (nodep2.type is not NodeType.SENSOR and # Don't allow SENSORS to get input
                    not gene.link.inode is node1 and
                    gene.link.onode is node2 and
                    gene.link.recurrent):
                        # Didn't make to the end of genes

                        tryCount += 1
                        break

                else:
                    # Made to the end of genes

                    count = 0
                    isRecurrent = self.phenotype.isRecurrent(node1.analogue, node2.analogue, count, thresh)

                    # ADDED: CONSIDER connections out of outputs recurrent
                    if (
                    node1.type == NodeType.OUTPUT or
                    node2.type == NodeType.OUTPUT
                    ):
                        isRecurrent = True

                    # Make sure it finds the right kind of link (recur)
                    if not isRecurrent:
                        tryCount += 1
                    else:
                        tryCount = tries
                        found = True


        else:
            # Loop to find a nonrecurrent link
            while tryCount < tries:

                # Chose random nodes
                node1 = choice(self.nodes)
                node2 = choice(self.nodes[firstNonSensor:])

                # See if a recurrent link already exists  ALSO STOP AT END OF GENES!!!!
                for gene in self.genes:

                    if not (nodep2.type is not NodeType.SENSOR and # Don't allow SENSORS to get input
                    not gene.link.inode is node1 and
                    gene.link.onode is node2 and
                    gene.link.recurrent):
                        # Didn't make to the end of genes

                        tryCount += 1
                        break

                else:
                    # Made to the end of genes

                    count = 0
                    isRecurrent = self.phenotype.isRecurrent(node1.analogue, node2.analogue, count, thresh)

                    # ADDED: CONSIDER connections out of outputs recurrent
                    if (
                    node1.type == NodeType.OUTPUT or
                    node2.type == NodeType.OUTPUT
                    ):
                        isRecurrent = True

                    # Make sure it finds the right kind of link (recur)
                    if not isRecurrent:
                        tryCount += 1
                    else:
                        tryCount = tries
                        found = True

            # End of normal link finding loop

        if found:

            # If it was supposed to be recurrent, make sure it gets labeled that way
            if recurrent:
                isRecurrent = True

            # loop to find a non recurrent link
            for innovation in innovations:
                pass
            # The innovation is totally novel
            else:
                # If the phenotype does not exist, exit
                if phenotype == 0:
                    vprint(1, 'Error: Attempt to add link to genome with no phenotype')
                    return None

                # Choose a random trait
                trait = choice(self.traits)

                # Choose the new weight
                newWeight = uniform(-1, 1)

                # Create the new gene
                newGene = Gene(
                    trait=trait,
                    weight=newWeight,
                    inode=node1,
                    onode=node2,
                    recurrent=isRecurrent,
                    innovation=currentInnovationNumber,
                    mutation=newWeight
                )

                # Add the innovation
                innovations.append(Innovation(
                    inode=node1.id,
                    onode=node2.id,
                    innovation=currentInnovationNumber,
                    weight=newWeight,
                    trait=trait
                ))





        raise NotImplementedError


    # Mutate genome by adding a sensor node
    def mutateAddSensor(self, innovations: List[Innovation], currentInnovationNumber: int) -> None:
        raise NotImplementedError


    # Adds a new gene that has been created through a mutation
    def addGene(self, genes: List[Gene], gene: Gene) -> None:
        raise NotImplementedError


    # Inserts a Node into a given ordered list of Nodes in order
    def insertNode(self, nodes: List[Node], node: Node) -> None:
        raise NotImplementedError


    # This method mates this Genome with another genome.
    def mateMultipoint(self, genome: Genome, fitness1: float, fitness2: float) -> Genome:
        raise NotImplementedError


    # This method mates like multipoint but instead of selecting one it averages their weights
    def mateMultipointAverage(self, genome: Genome, fitness1: float, fitness2: float) -> Genome:
        raise NotImplementedError


    # This method is similar to a standard single point CROSSOVER operator.
    def mateSinglepoint(self, genome: Genome) -> Genome:
        raise NotImplementedError


    # This function gives a measure of compatibility between two Genomes
    def compatibility(self, genome: Genome) -> float:

        maxSize = max(len(self.genes), len(genome.genes))
        excess = abs(len(self.genes) - len(genome.genes))
        matching = 0
        disjoint = 0
        mutationDifference = 0

        i1 = 0
        i2 = 0

        while i1 != len(self.genes) and i2 != len(genome.genes):

            gene1 = self.genes[i1]
            gene2 = genome.genes[i2]

            if gene1.innovation == gene2.innovation:
                matching += 1
                mutationDifference += abs(gene1.mutation - gene2.mutation)

                i1 += 1
                i2 += 1

            elif gene1.innovation > gene2.innovation:
                disjoint += 1

                i2 += 1

            elif gene1.innovation < gene2.innovation:
                disjoint += 1

                i1 += 1

        return (neat.disjointCoefficient * disjoint +
        neat.excessCoefficient * excess +
        neat.mutationDifferenceCoefficient * mutationDifference / matching)


    # This function compares two traits named trait1 and trait2
    def compareTrait(self, trait1: Trait, trait2: Trait) -> float:
        raise NotImplementedError


    # Return number of non-disabled genes
    def extrons(self) -> int:
        raise NotImplementedError


    # Randomize the trait pointers of all the node and connection genes
    def randomizeTraits(self) -> None:

        # Go through all nodes and randomize their trait pointers
        for node in self.nodes:
            trait = choice(self.traits)
            node.trait = trait

        # Go through all connections and randomize their trait pointers
        for gene in self.genes:
            trait = choice(self.traits)
            gene.link.trait = trait
