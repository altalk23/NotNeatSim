from __future__ import annotations

from typing import Dict, List

from organism import *
from population import *

class Specie:

    # Variable annotations
    id: int = 0
    age: int = 0

    averageFitness: float = 0
    maximumFitness: float = 0
    maxiumTotalFitness: float = 0

    expectedOffspring: int = 0
    ageOfLastImprovement: int = 0
    averageEstimated: float = 0

    novel: bool = False
    checked: bool = False
    obliterate: bool = False

    organisms: List[Organism] = []


    def __init__(self,
    id: int = None,
    novel: bool = False,
    data: Dict[str, object] = None) -> None:

        self.age = 1

        # Creates a specie
        if (id is not None):
            self.id = id
            self.novel = novel

        # Generate the object from dict
        elif (data is not None):
            raise NotImplementedError


    # Return the dict representation of the object
    def toDict(self) -> Dict[str, object]:
        raise NotImplementedError


    # Change the fitness of all the organisms in the specie
    def adjustFitness(self) -> None:
        raise NotImplementedError


    # Computes the average fitness of the specie
    def computeAverageFitness(self) -> None:
        self.averageFitness = sum(org.fitness for org in self.organisms) / len(self.organisms)


    # Computes the maximum fitness of the specie
    def computeMaximumFitness(self) -> None:
        self.maximumFitness = max(org.fitness for org in self.organisms)


    # Counts the number of offspring expected from all its members
    def countOffspring(self, skim: float) -> float:
        raise NotImplementedError


    # Compute generations since last improvement
    def lastImproved(self) -> int:
        return age - ageOfLastImprovement


    # Returns the champion of the specie
    def getChampion(self) -> Organism:
        raise NotImplementedError


    # Perform mating and mutation to form next generation
    def reproduce(self, generation: int, population: Population, sortedSpecies: List[Specie]) -> None:
        raise NotImplementedError


    # Place organisms in this specie in order by their fitness
    def rank(self) -> None:
        self.organisms.sort(key = lambda org: org.fitness, reverse = True)


    # Compute an estimate of the average fitness of the specie
    def estimateAverage(self) -> float:
        raise NotImplementedError


    # Like the usual reproduce method except only one offspring is produced
    def reproduceOne(self, generation: int, population: Population, sortedSpecies: List[Specie]) -> None:
        raise NotImplementedError
