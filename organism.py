from __future__ import annotations

from typing import Dict

from genome import *
from network import *
from specie import *

class Organism:

    # Variable annotations
    fitness: float
    originalFitness: float
    error: float

    genome: Genome
    nework: Network
    specie: Specie

    expectedOffspring: float
    superChampionOffspring: int

    generation: int

    winner: bool
    eliminate: bool
    champion: bool

    populationChampion: bool
    populationChampionChild: bool

    timeAlive: int

    mateBaby: bool
    mutationStructureBaby: bool

    metadata: str

    def __init__(self,
    fitness: int = None,
    genome: Genome = None,
    metadata: str = '',
    generation: int = None,
    data: Dict[str, object] = None) -> None:

        # Initialize organism from fit, genome and generation number
        if (fitness is not None and
        genome is not None and
        generation is not None):

            self.specie = None
            self.expectedOffspring = 0
            self.superChampionOffspring = 0
            self.eliminate = False
            self.winner = False
            self.champion = False
            self.error = 0
            self.timeAlive = 0
            # debug?
            self.mateBaby = False
            self.mutationStructureBaby = False
            self.populationChampion = False
            self.populationChampionChild = False

            self.fitness = fitness
            self.originalFitness = fitness
            self.genome = genome
            self.generation = generation
            self.metadata = metadata

            self.network = genome.genesis(genome.id)



        # Generate the object from dict
        elif (data is not None):
            raise NotImplementedError


    # Return the dict representation of the object
    def toDict(self) -> Dict[str, object]:
        raise NotImplementedError


    # Regenerate the network based on a change in the genotype
    def updatePhenotype(self):
        raise NotImplementedError
