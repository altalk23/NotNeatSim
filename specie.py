from __future__ import annotations

from math import floor
from random import choice, random
from typing import Dict, List

from mutator import *
from network import *
import organism as org
from population import *
import neat

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

    organisms: List[org.Organism] = []


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

        vprint(3, f'Species {self.id} last improved  {self.age - self.ageOfLastImprovement} steps ago when it moved up to {self.maxiumTotalFitness}')

        ageDebt = self.age - self.ageOfLastImprovement + 1 - neat.dropoffAge
        if ageDebt == 0:
            ageDebt = 1

        for organism in self.organisms:

            # Remember the original fitness before it gets modified
            organism.originalFitness = organism.fitness

            # Make fitness decrease after a stagnation point dropoff age
            if ageDebt >= 1 or self.obliterate:
                # Extreme penalty for a long period of stagnation (divide fitness by 100)
                organism.fitness /= 100

            # Give a fitness boost up to some young age (niching)
            if self.age <= 10:
                organism.fitness *= neat.ageSignificance

            # Do not allow negative fitness
            organism.fitness = max(organism.fitness, 0.0001)

            # Share fitness with the species
            organism.fitness /= len(self.organisms)

        # Sort the population based on fitness
        self.organisms.sort(key=lambda org: org.fitness, reverse=True)

        # Update ageOfLastImprovement here
        if self.organisms[0].originalFitness > self.maxiumTotalFitness:
            self.ageOfLastImprovement = self.age
            self.maxiumTotalFitness = self.organisms[0].originalFitness

        # Decide how many get to reproduce based on survival threshold * population size
        numberOfParents = floor(neat.survivalThreshold * len(self.organisms))

        # Mark for death those who are ranked too low to be parents
        self.organisms[0].champion = True
        for organism in self.organisms[1:]:
            if numberOfParents:
                numberOfParents -= 1
            else:
                organism.eliminate = True


    # Computes the average fitness of the specie
    def computeAverageFitness(self) -> None:
        self.averageFitness = sum(org.fitness for org in self.organisms) / len(self.organisms)


    # Computes the maximum fitness of the specie
    def computeMaximumFitness(self) -> None:
        self.maximumFitness = max(org.fitness for org in self.organisms)


    """
    CODED BY BIRKIY
    """
    # Counts the number of offspring expected from all its members
    def countOffspring(self, skim: float) -> float:

        expectedOffspring = 0

        for organism in self.organisms:
            expectedOffspring += organism.expectedOffspring // 1

            skim += organism.expectedOffspring % 1

            # NOTE:  Some precision is lost by computer
		    #        Must be remedied later

            if skim > 0:
                expectedOffspring += skim // 1
                skim -= skim // 1

        return skim


    # Compute generations since last improvement
    def lastImproved(self) -> int:
        return age - ageOfLastImprovement


    """
    CODED BY BIRKIY
    """
    # Returns the champion of the specie
    def getChampion(self) -> org.Organism:
        champFitness: float = -1.0
        champion: org.Organism

        for organism in self.organisms:
            vprint(3, f'Searching for champ... {organism.genome.id} fitness: {organism.fitness}')

            if organism.fitness > champFitness:
                champion = organism
                champFitness = champion.fitness

        vprint(3, f'Returning champ #{champion.genome.id}')

        return champion


    # Perform mating and mutation to form next generation
    def reproduce(self, generation: int, population: Population, sortedSpecies: List[Specie]) -> None:

        # Variable annotations

        mom: org.Organism # Parent Organisms
        dad: org.Organism
        baby: org.Organism # The new Organism

        newGenome: Genome # For holding baby's genes
        newSpecie: Specie # For babies in new specie

        randomOrganism: org.Organism # Random organism
        randomSpecie: Specie # For mating outside the specie
        randomMultiplier: float

        networkAnalogue: Network # For adding link to test for recurrency

        pause: int
        outside: bool
        found: bool # When a specie is found
        giveup: int # For giving up finding a mate outside the species

        champion: org.Organism = None
        championDone: bool = False # Flag the preservation of the champion

        mutationStructureBaby: bool
        mateBaby: bool

        poolSize: int # The number of Organisms in the old generation

        totalFitness: float = 0
        marble: float # The marble will have a number between 0 and totalFitness
        spin: float # Fitness total while the wheel is spinning


        if self.expectedOffspring > 0 and len(self.organisms) == 0:
            vprint(1, 'Error: Attempt to reproduce out of empty specie')

        else:

            poolSize = len(self.organisms) - 1

            champion = self.organisms[0]

            for count in range(self.expectedOffspring):
                outside = False
                mutationStructureBaby = False
                mateBaby = False

                # If we have a super_champ (Population champion), finish off some special clones
                if champion.superChampionOffspring > 0:
                    mom = champion
                    newGenome = mom.genome.duplicate(count)

                    # Most superchamp offspring will have their connection weights mutated only
                    if champion.superChampionOffspring > 1:
                        if random() < 0.8 or neat.mutateAddLinkProbability == 0:
                            newGenome.mutateLinkWeights(neat.weightMutationPower, 1, Mutator.GAUSSIAN)
                        else:
                            # Sometimes we add a link to a superchamp
                            networkAnalogue = newGenome.genesis(generation)
                            newGenome.mutateAddLink(population.innovations, population.currentInnovationNumber, neat.newLinkTries)
                            networkAnalogue = None
                            mutationStructureBaby = True

                    baby = org.Organism(fitness=0, genome=newGenome, generation=generation)

                    if champion.superChampionOffspring == 1:
                        if champion.populationChampion:
                            baby.populationChampionChild = True
                            baby.highestFitness = mom.originalFitness

                    champion.superChampionOffspring -= 1

                # If we have a Species champion, just clone it
                elif not championDone and self.expectedOffspring > 5:
                    mom = champion
                    newGenome = mom.genome.duplicate(count)

                    # Baby is just like mommy
                    baby = org.Organism(fitness=0, genome=newGenome, generation=generation)

                    championDone = True

                # First, decide whether to mate or mutate, if there is only one organism in the pool, then always mutate
                elif random() < neat.mutateOnlyProbability or poolSize == 0:
                    # Choose the random parent
                    mom = choice(self.organisms)
                    newGenome = mom.genome.duplicate(count)

                    # Do the mutation depending on probabilities of various mutations
                    if random() < neat.mutateAddNodeProbability:
                        newGenome.mutateAddNode(population.innovations, population.currentNodeId, population.currentInnovationNumber)
                        mutationStructureBaby = True

                    elif random() < neat.mutateAddLinkProbability:
                        networkAnalogue = newGenome.genesis(generation)
                        newGenome.mutateAddLink(population.innovations, population.currentInnovationNumber, neat.newLinkTries)
                        networkAnalogue = None
                        mutationStructureBaby = True

                    else:
                        # If we didn't do a structural mutation, we do the other kinds
                        if random() < neat.mutateRandomTraitProbability:
                            newGenome.mutateRandomTrait()

                        if random() < neat.mutateLinkTraitProbability:
                            newGenome.mutateLinkTrait(1)

                        if random() < neat.mutateNodeTraitProbability:
                            newGenome.mutateNodeTrait(1)

                        if random() < neat.mutateLinkWeightsProbability:
                            newGenome.mutateLinkWeights(neat.weightMutationPower, 1, Mutator.GAUSSIAN)

                        if random() < neat.mutateToggleEnableProbability:
                            newGenome.mutateToggleEnable(1)

                        if random() < neat.mutateGeneReenableProbability:
                            newGenome.mutateGeneReenable()

                    baby = org.Organism(fitness=0, genome=newGenome, generation=generation)

                # Otherwise we should mate
                else:
                    # Choose the random mom
                    mom = choice(self.organisms)

                    # Choose random dad
                    if random() > neat.interspeciesMateRate:
                        # Mate within Species
                        dad = choice(self.organisms)

                    # Mate outside specie
                    else:
                        randomSpecie = self

                        # Select a random specie
                        for _ in range(5):
                            if randomSpecie is self:
                                # Choose a random specie tending towards better specie
                                randomMultiplier = min(neat.gaussrand() / 4, 1)
                                randomSpecieNum = floor(randomMultiplier * (len(sortedSpecies) - 1) + 0.5)
                                randomSpecie = sortedSpecies[randomSpecieNum]
                            else:
                                break

                            # New way: Make dad be a champ from the random species
                            dad = randomSpecie.organisms[0]
                            outside = True

                        # Perform mating based on probabilities of differrent mating types
                        if random() < neat.mateMultipointProbability:
                            newGenome = mom.genome.mateMultipoint(dad.genome, count, mom.originalFitness, dad.originalFitness, outside)
                        elif random() < neat.mateMultipointAverageProbability / (neat.mateMultipointAverageProbability + neat.mateSinglepointProbability):
                            newGenome = mom.genome.mateMultipointAverage(dad.genome, count, mom.originalFitness, dad.originalFitness, outside)
                        else:
                            newGenome = mom.genome.mateSinglepoint(dad.genome, count)

                        mateBaby = True

                        # Determine whether to mutate the baby's Genome
                        if random() > neat.mateOnlyProbability or dad.genome.id == mom.genome.id or dad.genome.compatibility(mom.genome) == 0:
                            # This is done randomly or if the mom and dad are the same organism

                            # Copied from above

                            # Do the mutation depending on probabilities of various mutations
                            if random() < neat.mutateAddNodeProbability:
                                newGenome.mutateAddNode(population.innovations, population.currentNodeId, population.currentInnovationNumber)
                                mutationStructureBaby = True

                            elif random() < neat.mutateAddLinkProbability:
                                networkAnalogue = newGenome.genesis(generation)
                                newGenome.mutateAddLink(population.innovations, population.currentInnovationNumber, neat.newLinkTries)
                                networkAnalogue = None
                                mutationStructureBaby = True

                            else:
                                # If we didn't do a structural mutation, we do the other kinds
                                if random() < neat.mutateRandomTraitProbability:
                                    newGenome.mutateRandomTrait()

                                if random() < neat.mutateLinkTraitProbability:
                                    newGenome.mutateLinkTrait(1)

                                if random() < neat.mutateNodeTraitProbability:
                                    newGenome.mutateNodeTrait(1)

                                if random() < neat.mutateLinkWeightsProbability:
                                    newGenome.mutateLinkWeights(neat.weightMutationPower, 1, Mutator.GAUSSIAN)

                                if random() < neat.mutateToggleEnableProbability:
                                    newGenome.mutateToggleEnable(1)

                                if random() < neat.mutateGeneReenableProbability:
                                    newGenome.mutateGeneReenable()

                        baby = org.Organism(fitness=0, genome=newGenome, generation=generation)

                # Add the baby to its proper Species
                # If it doesn't fit a Species, create a new one

                baby.mutationStructureBaby = mutationStructureBaby
                baby.mateBaby = mateBaby

                # Create the first species
                if len(population.species) == 0:
                    population.currentSpecieId += 1
                    newSpecie = Specie(id=population.currentSpecieId, novel=True)
                    population.species.append(newSpecie)
                    newSpecie.organisms.append(baby)
                    baby.specie = newSpecie

                else:

                    # Search for each specie
                    for specie in population.species:
                        compareOrganism = specie.organisms[0]

                        # Found compatible specie, add organism to specie
                        if baby.genome.compatibility(compareOrganism.genome) < neat.compatibilityThreshold:
                            specie.organisms.append(baby)
                            baby.specie = specie
                            break

                    # Didn't find a match, create new specie
                    else:
                        # Create the new specie
                        population.currentSpecieId += 1
                        newSpecie = Specie(id=population.currentSpecieId, novel=True)
                        self.species.append(newSpecie)
                        newSpecie.organisms.append(baby)
                        baby.specie = newSpecie



    # Place organisms in this specie in order by their fitness
    def rank(self) -> None:
        self.organisms.sort(key = lambda org: org.fitness, reverse = True)


    """
    CODED BY BIRKIY
    """
    # Compute an estimate of the average fitness of the specie
    def estimateAverage(self) -> float:
        total: float = 0 # running total of fitnesses

        # Note: Since evolution is happening in real-time, some organisms may not
    	# have been around long enough to count them in the fitness evaluation

        numOrg: float = 0 # counts number of orgs above the time_alive threshold

        for organism in self.organisms:
            if organism.timeAlive >= neat.timeAliveMinimum:
                total += organism.fitness

            if numOrg > 0:
                averageEst = total / numOrg
            else:
                averageEst = 0

        return averageEst


    # Like the usual reproduce method except only one offspring is produced
    def reproduceOne(self, generation: int, population: Population, sortedSpecies: List[Specie]) -> None:
        raise NotImplementedError
