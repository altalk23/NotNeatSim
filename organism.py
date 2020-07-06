from __future__ import annotations

from typing import Dict

from genome import Genome
from network import Network
from specie import Specie

class Organism:

    # Variable annotations
    fitness: float
    originalFitness: float
    error: float

    genome: Genome
    nework: Network
    specie: Specie

    expectedOffspring: double
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
    fit: int = None,
    genome: Genome = None,
    generation: int = None,
    data: Dict[str, object] = None) -> None:

        # Initialize organism from fit, genome and generation number
        if (fit is not None and
        genome is not None and
        generation is not None):
            raise NotImplementedError

        # Generate the object from dict
        elif (data is not None):
            raise NotImplementedError


    # Return the dict representation of the object
    def toDict(self) -> Dict[str, object]:
        raise NotImplementedError


    # Regenerate the network based on a change in the genotype
    def updatePhenotype(self):
        raise NotImplementedError
