from __future__ import annotations

from typing import Dict, List

from mutator import *
from network import *

class Genome:

    # Variable annotations
    id: int

    traits: List[Trait]
    genes: List[Gene]
    nodes: List[Node]

    phenotype: Network


    def __init__(self,
    config: Dict[str, object] = None,
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
    type: int = None) -> None:

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

        # Special constructor which spawns off an input file
        elif (config is not None):
            raise NotImplementedError


    # Loads a new Genome from a file
    def newGenomeLoad(self, filename: str) -> Genome:
        raise NotImplementedError


    # Generate a network phenotype from this Genome with specified id
    def genesis(self, id: int) -> Newtork:
        raise NotImplementedError


    # For debugging: A number of tests can be run on a genome to check its integrity
    def verify(self) -> bool:
        raise NotImplementedError


    # Dump this genome to specified file
    def printToFile(self, filename: str) -> None:
        raise NotImplementedError


    # Dump this genome to a dict object
    def toDict(self) -> Dict[str, object]:
        raise NotImplementedError


    # Duplicate this Genome to create a new one with the specified id
    def duplicate(self, id: int) -> Genome:
        raise NotImplementedError


    # Return id of final Node in Genome
    def getLastNodeId(self) -> int:
        raise NotImplementedError


    # Return last innovation number in Genome
    def getLastGeneInnovnum(self) -> double:
        raise NotImplementedError


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
        raise NotImplementedError


    # Toggle genes on or off
    def mutateToggleEnable(self, count: int) -> None:
        raise NotImplementedError


    # Find first disabled gene and enable it
    def mutateGeneReenable(self) -> None:
        raise NotImplementedError


    # Mutate genome by adding a node respresentation
    def mutateAddNode(self, innovations: List[Innovation], currentInnovationNumber: int, currentNodeId: int) -> None:
        raise NotImplementedError


    # Mutate the genome by adding a new link between 2 random nodes
    def mutateAddLink(self, innovations: List[Innovation], currentInnovationNumber: int, tries: int) -> None:
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
        raise NotImplementedError


    # This function compares two traits named trait1 and trait2
    def compareTrait(self, trait1: Trait, trait2: Trait) -> float:
        raise NotImplementedError


    # Return number of non-disabled genes
    def extrons(self) -> int:
        raise NotImplementedError


    # Randomize the trait pointers of all the node and connection genes
    def randomizeTraits(self) -> None:
        raise NotImplementedError
