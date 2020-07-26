from __future__ import annotations

from math import ceil, floor
from random import random
from typing import Dict, List

from yaml import dump

import neat
import organism
import specie as sp
from genome import *
from innovation import *
from mutator import *
from print import *

class Population:

    # Variable annotations
    organisms: List[Organism]
    species: List[Specie]
    innovations: List[Innovation]

    currentNodeId: int
    currentSpecieId: int
    currentInnovationNumber: int

    meanFitness: float
    variance: float
    standardDeviation: float
    highestFitness: float
    highestLastChanged: float

    winnerGeneration: int


    def __init__(self,
    genome: Genome = None,
    size: int = None,
    power: float = None,

    data: Dict[str, object] = None) -> None:

        self.organisms = []
        self.species = []
        self.innovations = []

        # Construct off of a single spawning Genome without mutation
        if (genome is not None and
        size is not None and
        power is not None):
            raise NotImplementedError

        # Construct off of a single spawning Genome
        elif (genome is not None and
        size is not None):
            self.winnerGeneration = 0
            self.highestFitness = 0.0
            self.highestLastChanged = 0
            self.spawn(genome, size)

        # Generate the object from dict
        elif (data is not None):
            raise NotImplementedError


    # Return the dict representation of the object
    def toDict(self) -> Dict[str, object]:
        raise NotImplementedError


    # A Population can be spawned off of a single Genome
    def spawn(self, genome: Genome, size: int) -> None:

        # Variable annotations
        count: int
        newGenome: Genome
        newOrganism: organism.Organism

        # Create copies of the genome
        for count in range(1, size+1):
            newGenome = genome.duplicate(count)
            newGenome.mutateLinkWeights(1.0, 1.0, Mutator.COLDGAUSSIAN)
            newGenome.randomizeTraits()

            newOrganism = organism.Organism(fitness=0.0, genome=newGenome, generation=1);
            self.organisms.append(newOrganism)

        # Store the current node id and innovation number
        self.currentNodeId = newGenome.getLastNodeId()
        self.currentInnovationNumber = newGenome.getLastInnovationNumber()

        # Split the population into species
        self.speciate()


    # Separate the Organisms into species
    def speciate(self) -> None:

        # Variable annotations
        compareOrganism: organism.Organism
        newSpecie: sp.Specie

        # Loop for each organism
        for organism in self.organisms:

            # Search for each specie
            for specie in self.species:
                compareOrganism = specie.organisms[0]

                # Found compatible specie, add organism to specie
                if organism.genome.compatibility(compareOrganism.genome) < neat.compatibilityThreshold:
                    specie.organisms.append(organism)
                    organism.specie = specie
                    break

            # Didn't find a match, create new specie
            else:
                # Create the new specie
                newSpecie = sp.Specie(id=len(self.species) + 1)
                self.species.append(newSpecie)
                newSpecie.organisms.append(organism)
                organism.specie = newSpecie

        self.currentSpecieId = len(self.species)


    # Certified UwU moment
    def printToFile(self, experimentNumber: int, generationNumber: int) -> None:
        raise DeprecationWarning

        with open(f'output/Population #{experimentNumber}.{generationNumber}') as file:
            species = []

            # Add specie content
            for specie in self.species:
                species.append(specie.toDict())

            # Write to file
            yaml.dump({
                'experimentNumber': experimentNumber,
                'generationNumber': generationNumber,
                'species': species
            }, file)


    # Turnover the population to a new generation using fitness
    def epoch(self, generation: int) -> None:

        # Variable annotations

        # Fitness among all organisms
        totalFitness: int = 0
        averageFitness: int

        # Species sorted by maximum fitness
        sortedSpecies: List[Specie]

        # Specie constants
        targetNumberOfSpecies: int = 4;
        compatibilityMod: float = 0.3

        # Print the current generation
        vprint(2, f'Generation #{generation}:')


        # Sort the species by maximum fitness (using original fitness)
        sortedSpecies = sorted(self.species, key=lambda sp: sp.organisms[0].originalFitness, reverse=True)


        # Flag the lowest performing species over age 20 every 30 generations
        if generation % 30 == 0:
            for specie in reversed(sortedSpecies):
                if specie.age >= 20:
                    specie.obliterate = True
                    break

        vprint(2, f'Number of Species: {len(self.species)}')
        vprint(2, f'Compatibility Mod: {compatibilityMod}')


        # Adjust species' fitnesses using their ages
        for specie in self.species:
            specie.adjustFitness()


        # TODO: Cleanup this code vv

        # Go through the organisms and add up their fitnesses to compute the overall average
        for organism in self.organisms:
            totalFitness += organism.fitness
        averageFitness = totalFitness / len(self.organisms)

        vprint(2, f'Overall Average Fitness: {averageFitness}')


        # TODO: Cleanup this code vv

        # Compute the expected number of offspring for each individual organism
        for organism in self.organisms:
            organism.expectedOffspring = organism.fitness / averageFitness
            #print(f"id: {organism.genome.id} offspring: {organism.expectedOffspring}")

        # Sort the species by maximum fitness (using original fitness)
        sortedSpecies = sorted(self.species, key=lambda sp: sp.organisms[0].originalFitness, reverse=True)

        # Now add those offspring up within each specie to get the number of offspring per specie
        precisionSkim: float = 0.0
        totalOffspring: int = 0
        for specie in sortedSpecies:
            precisionSkim = specie.countOffspring(precisionSkim)
            totalOffspring += specie.expectedOffspring

        # If we lost precision, give an extra baby to the best Species
        if totalOffspring < len(self.organisms):
            totalOffspring += 1
            sortedSpecies[0].expectedOffspring += 1

        # Achievement get: How Did We Get Here
        if totalOffspring < len(self.organisms):
            for specie in self.species:
                if specie is sortedSpecies[0]:
                    specie.expectedOffspring = len(self.organisms)
                else:
                    specie.expectedOffspring = 0

        # Print out for debugging
        for specie in sortedSpecies:
            vprint(2, f'Specie #{specie.id}, Size {len(specie.organisms)}')
            vprint(2, f'Original fitness: {specie.organisms[0].originalFitness}')
            vprint(2, f'Last improved: {specie.age - specie.ageOfLastImprovement}')


        # TODO: Cleanup this code vv

        # Check for Population-level stagnation
        sortedSpecies[0].organisms[0].populationChampion = True
        if sortedSpecies[0].organisms[0].originalFitness > self.highestFitness:
            self.highestFitness = sortedSpecies[0].organisms[0].originalFitness
            self.highestLastChanged = 0
            vprint(1, f'New Population Record Fitness: {self.highestFitness}')
            vprint(1, f'Output list: {sortedSpecies[0].organisms[0].network.outputList}')
            vprint(1, f'Node count: {len(sortedSpecies[0].organisms[0].network.nodes)}')
            sortedSpecies[0].organisms[0].genome.print()
            vprint(1, f'')
        else:
            self.highestLastChanged += 1
            vprint(2, f'{self.highestLastChanged} generations since last population fitness record: {self.highestFitness}')


        # TODO: Cleanup this code vv

        # Check for stagnation- if there is stagnation, perform delta-coding
        if self.highestLastChanged >= neat.dropoffAge + 5:
            vprint(3, f'Performing delta coding')
            self.highestLastChanged = 0


            if len(sortedSpecies) < 2:
                sortedSpecies[0].organisms[0].superChampionOffspring = neat.populationSize
                sortedSpecies[0].expectedOffspring = neat.populationSize
                sortedSpecies[0].ageOfLastImprovement = sortedSpecies[0].age
            else:
                for specie in sortedSpecies:
                    if specie is sortedSpecies[0]:
                        specie.organisms[0].superChampionOffspring = ceil(neat.populationSize / 2)
                        specie.expectedOffspring = ceil(neat.populationSize / 2)
                        specie.ageOfLastImprovement = specie.age

                    elif specie is sortedSpecies[1]:
                        specie.organisms[0].superChampionOffspring = floor(neat.populationSize / 2)
                        specie.expectedOffspring = floor(neat.populationSize / 2)
                        specie.ageOfLastImprovement = specie.age

                    else:
                        specie.expectedOffspring = 0

        # TODO: Cleanup this code vv

        # STOLEN BABIES:  The system can take expected offspring away from
        # worse species and give them to superior species
        elif neat.babiesStolen > 0:

            # Take away a constant number of expected offspring from the worst few species
            stolenBabies = 0

            for specie in reversed(sortedSpecies):
                if specie.age > 5 and specie.expectedOffspring > 2:
                    vprint(3, f'Stealing')

                    # Enough the finish the pool
                    if specie.expectedOffspring > neat.babiesStolen - stolenBabies:
                        specie.expectedOffspring -= neat.babiesStolen - stolenBabies
                        stolenBabies = neat.babiesStolen
                        break

                    # Not enough to finish the pool
                    else:
                        stolenBabies += specie.expectedOffspring - 1
                        specie.expectedOffspring = 1


            specieIter = iter(sortedSpecies)

            try:
                # Skip dying species
                specie = next(specieIter)
                while specie.lastImproved() > neat.dropoffAge:
                    specie = next(specieIter)

                # First specie
                if stolenBabies >= neat.babiesStolen // 5:
                    specie.organisms[0].superChampionOffspring += neat.babiesStolen // 5
                    specie.expectedOffspring += neat.babiesStolen // 5
                    stolenBabies -= neat.babiesStolen // 5

                # Skip dying species
                specie = next(specieIter)
                while specie.lastImproved() > neat.dropoffAge:
                    specie = next(specieIter)

                # Second specie
                if stolenBabies >= neat.babiesStolen // 5:
                    specie.organisms[0].superChampionOffspring += neat.babiesStolen // 5
                    specie.expectedOffspring += neat.babiesStolen // 5
                    stolenBabies -= neat.babiesStolen // 5

                # Skip dying species
                specie = next(specieIter)
                while specie.lastImproved() > neat.dropoffAge:
                    specie = next(specieIter)

                # Third specie
                if stolenBabies >= neat.babiesStolen // 10:
                    specie.organisms[0].superChampionOffspring += neat.babiesStolen // 10
                    specie.expectedOffspring += neat.babiesStolen // 10
                    stolenBabies -= neat.babiesStolen // 10

                # Skip dying species
                specie = next(specieIter)
                while specie.lastImproved() > neat.dropoffAge:
                    specie = next(specieIter)

                while stolenBabies > 0:
                    # Randomize a little

                    if random() > 0.1:
                        specie.organisms[0].superChampionOffspring += min(3, stolenBabies)
                        specie.expectedOffspring += min(3, stolenBabies)
                        stolenBabies -= min(3, stolenBabies)

                    # Skip dying species
                    specie = next(specieIter)
                    while specie.lastImproved() > neat.dropoffAge:
                        specie = next(specieIter)


            except StopIteration:

                # If any stolen babies aren't taken, give them to species #1's champ
                if stolenBabies > 0:
                    vprint(3, f'Not all given back, giving to best Species')

                    sortedSpecies[0].organisms[0].superChampionOffspring += stolenBabies
                    sortedSpecies[0].expectedOffspring += stolenBabies
                    stolenBabies = 0


        # Kill of all organism marked for death
        organismKill = reversed(list(enumerate(self.organisms.copy())))
        for index, organism in organismKill:
            if organism.eliminate:
                organism.specie.organisms.remove(organism)
                del self.organisms[index]


        # Perform reproduction. Reproduction is done on a per-specie basis.
        for specie in self.species.copy():
            specie.reproduce(generation, self, sortedSpecies)

        vprint(3, f'Reproduction Complete')

        # Destroy and remove the old generation from the organisms and species
        for organism in self.organisms:
            organism.specie.organisms.remove(organism)
        self.organisms = []

        # Remove all empty Species and age ones that survive
        organismCount = 0
        specieKill = reversed(list(enumerate(self.species.copy())))

        for index, specie in specieKill:
            # Remove the specie if empty
            if len(specie.organisms) < 1:
                del self.species[index]

            # Age any Species that is not newly created in this generation
            else:
                self.species[index].age += 1

                # Add them to the master list
                for organism in specie.organisms:
                    organism.genome.id = organismCount
                    organismCount += 1
                    self.organisms.append(organism)


        # Epoch completed
        vprint(2, f'Epoch completed\n\n\n\n')


    # why
    def verify(self) -> None:
        raise NotImplementedError


    # Places the organisms in species in order from best to worst fitness
    def rankWithinSpecies(self) -> None:
        raise NotImplementedError


    # Estimates average fitness for all existing species
    def estimateAllAverages(self) -> None:
        raise NotImplementedError


    # Probabilistically choose a species to reproduce
    def chooseParentSpecie(self) -> sp.Specie:
        raise NotImplementedError


    # Remove a specie from the species list
    def removeSpecie(self, specie: sp.Specie) -> None:
        raise NotImplementedError


    # Removes worst member of population that has been around
    def removeWorst(self) -> organism.Organism:
        raise NotImplementedError


    # Reproduce only out of the pop champ
    def reproduceChampion(self, generation: int) -> organism.Organism:
        raise NotImplementedError


    # This method takes an Organism and reassigns what Species it belongs to
    def reassignSpecie(self, organism: organism.Organism) -> None:
        raise NotImplementedError


    # Move an Organism from one Species to another (called by reassignSpecie)
    def switchSpecie(self, organism: organism.Organism, originalSpecie: sp.Specie, newSpecie: sp.Specie) -> None:
        raise NotImplementedError
