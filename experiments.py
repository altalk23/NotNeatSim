from __future__ import annotations

from typing import Dict, List

from yaml import load, Loader

import neat
from genome import *
from organism import *
from population import *
from print import *

def xorTest(generationCount: int) -> Population:

    # Variable annotations
    population: Population
    startGenome: Genome

    evals: List[int]
    genes: List[int]
    nodes: List[int]

    totalNodes: int = 0
    totalGenes: int = 0
    totalEvals: int = 0
    samples: int = 0 # Used for averaging




    # Start of XOR Test
    vprint(1, 'Start XOR Test')

    # Read the first genome
    vprint(1, 'Reading in the start genome')

    with open('xorstartgenome.yaml') as file:
        data = load(file, Loader=Loader)
        startGenome = Genome(data=data)


    for experimentNumber in range(neat.numberOfRuns):

        # Spawn the population
        vprint(1, 'Spawning the population')
        population = Population(genome=startGenome, size=neat.populationSize)

        # Verify the population
        vprint(1, 'Verifying the spawned population')
        #population.verify()

        for generationNumber in range(1, generationCount + 1):
            vprint(2, f'Epoch {generationNumber}')

            # Check for success
            epoch = xorEpoch(population, experimentNumber, generationNumber)
            if (epoch['passed']):
                evals[experimentNumber] = neat.populationSize * (generationNumber - 1) + epoch['winnerId']
                genes[experimentNumber] = epoch['winnerGenes']
                nodes[experimentNumber] = epoch['winnerNodes']
                break


        if experimentNumber < neat.numberOfRuns - 1:
            del population


    # Print statistics

    vprint(1, 'Nodes:')
    for experimentNumber in range(neat.numberOfRuns):
        vprint(2, nodes[experimentNumber])
        totalNodes += nodes[experimentNumber]


    vprint(1, 'Genes:')
    for experimentNumber in range(neat.numberOfRuns):
        vprint(2, genes[experimentNumber])
        totalGenes += genes[experimentNumber]


    vprint(1, 'Evals:')
    for experimentNumber in range(neat.numberOfRuns):
        vprint(2, evals[experimentNumber])
        if evals[experimentNumber] > 0:
            totalEvals += nodes[experimentNumber]
            samples += 1

    vprint(1, f'Failures: {neat.numberOfRuns - samples} out of {neat.numberOfRuns} runs')
    vprint(1, f'Average Nodes {0 if samples == 0 else totalNodes / samples}')
    vprint(1, f'Average Genes {0 if samples == 0 else totalGenes / samples}')
    vprint(1, f'Average Evals {0 if samples == 0 else totalEvals / samples}')



    return population



def xorEpoch(population: Population, experimentNumber: int, generationNumber: int) -> Dict[str, int]:

    # Variable annotations
    winnerId: int
    winnerNodes: int
    winnerGenes: int
    winnerOrganism: Organism
    passed: bool = False

    # Evaluate each organism
    for organism in population.organisms:
        if xorEvaluate(organism):
            passed = True
            winnerOrganism = organism
            winnerId = organism.genome.id
            winnerGenes = organism.genome.extrons()
            winnerNodes = len(organism.genome.nodes)


    # Average and max fitnesses of species
    for specie in population.species:
        specie.computeAverageFitness()
        specie.computeMaxFitness()


    # Print to file
    if passed:
        population.printToFile(experimentNumber, generationNumber)

        vprint(1, f'Winner is organism number {winnerId}')
        organism.printToFile(experimentNumber)

    population.epoch(generationNumber)

    if passed:
        return {
            'passed': True,
            'winnerId': winnerId,
            'winnerNodes': winnerNodes,
            'winnerGenes': winnerGenes
        }

    return {
        'passed': False
    }



def xorEvaluate(organism: Organism) -> bool:
    network: Network

    outputList: List[float] = []

    expectedOutputList: List[float] = [0.0, 1.0, 1.0, 0.0]
    successOutputThreshold: List[float] = [0.5, 0.5, 0.5, 0.5]

    # Check for successful activation
    success: bool

    # Used for figuring out how many nodes should be visited
    numberOfNodes: int

    # The maximum depth of the network
    networkDepth: int

    inputList: List[List[float]] = [
        [1.0, 0.0, 0.0],
        [1.0, 0.0, 1.0],
        [1.0, 1.0, 0.0],
        [1.0, 1.0, 1.0]
    ]

    network = organism.network

    numberOfNodes = len(organism.genome.nodes)
    networkDepth = network.maxDepth()

    # Load and activate the network for each input
    for input in inputList:
        network.loadSensors(input)

        success = network.activate()

        for relax in range(networkDepth + 1):
            success = network.activate()
            output = network.outputs[0].activation

        outputList.append(network.outputs[0].activation)

        network.flush()

    if success:
        errorsum = 0
        errorsum += abs(expectedOutputList[0] - outputList[0])
        errorsum += abs(expectedOutputList[1] - outputList[1])
        errorsum += abs(expectedOutputList[2] - outputList[2])
        errorsum += abs(expectedOutputList[3] - outputList[3])

        organism.fitness = (4.0 - errorsum) ** 2
        organism.error = errorsum

    else:
        # Flawed network
        errorsum = 999.0
        organism.fitness = 0.001

    vprint(3, f'Organism: {organism.genome.id}')
    vprint(3, f'Error: {outputList} -> {errorsum}')
    vprint(3, f'Fitness: {organism.fitness}')

    # Check if meets conditions
    if (
        abs(outputList[0] - expectedOutputList[0]) <= successOutputThreshold[0] and
        abs(outputList[1] - expectedOutputList[1]) <= successOutputThreshold[1] and
        abs(outputList[2] - expectedOutputList[2]) <= successOutputThreshold[2] and
        abs(outputList[3] - expectedOutputList[3]) <= successOutputThreshold[3]
    ):
        organism.winner = True
    else:
        organism.winner = False

    return organism.winner
