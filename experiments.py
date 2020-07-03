from typing import List, Dict

from yaml import load, Loader

from population import Population
from print import vprint
import neat

def xor_test(generation_count: int) -> Population:

    # Variable annotations
    population: Population
    start_genome: Genome

    evals: List[int]
    genes: List[int]
    nodes: List[int]

    total_nodes: int = 0
    total_genes: int = 0
    total_evals: int = 0
    samples: int = 0 # Used for averaging




    # Start of XOR Test
    vprint(1, 'Start XOR Test')

    # Read the first genome
    vprint(1, 'Reading in the start genome')

    with open('xorstartgenome.yaml') as file:
        config = load(file, Loader=Loader)
        start_genome = Genome(config=config)


    for experiment_number in range(neat.number_of_runs):

        # Spawn the population
        vprint(1, 'Spawning the population')
        population = Population(genome=start_genome, size=neat.population_size)

        # Verify the population
        vprint(1, 'Verifying the spawned population')
        population.verify()

        for generation_number in range(1, generation_count + 1):
            vprint(2, f'Epoch {generation_number}')

            # Check for success
            epoch = xor_epoch(population, experiment_number, generation_number)
            if (epoch['passed']):
                evals[experiment_number] = neat.population_size * (generation_number - 1) + epoch['winner_id']
                genes[experiment_number] = epoch['winner_genes']
                nodes[experiment_number] = epoch['winner_nodes']
                break


        if experiment_number < neat.number_of_runs - 1:
            del population


    # Print statistics

    vprint(1, 'Nodes:')
    for experiment_number in range(neat.number_of_runs):
        vprint(2, nodes[experiment_number])
        total_nodes += nodes[experiment_number]


    vprint(1, 'Genes:')
    for experiment_number in range(neat.number_of_runs):
        vprint(2, genes[experiment_number])
        total_genes += genes[experiment_number]


    vprint(1, 'Evals:')
    for experiment_number in range(neat.number_of_runs):
        vprint(2, evals[experiment_number])
        if evals[experiment_number] > 0:
            total_evals += nodes[experiment_number]
            samples += 1

    vprint(1, f'Failures: {neat.number_of_runs - samples} out of {neat.number_of_runs} runs')
    vprint(1, f'Average Nodes {0 if samples == 0 else total_nodes / samples}')
    vprint(1, f'Average Genes {0 if samples == 0 else total_genes / samples}')
    vprint(1, f'Average Evals {0 if samples == 0 else total_evals / samples}')



    return population



def xor_epoch(population: Population, experiment_number: int, generation_number: int) -> Dict[str, int]:

    # Variable annotations
    winner_id: int
    winner_nodes: int
    winner_genes: int
    winner_organism: Organism
    passed: bool = False

    # Evaluate each organism
    for organism in population.organisms:
        if xor_evaluate(organism):
            passed = True
            winner_organism = organism
            winner_id = organism.genome.id
            winner_genes = organism.genome.extrons()
            winner_nodes = len(organism.genome.nodes)


    # Average and max fitnesses of species
    for specie in population.species:
        specie.compute_average_fitness()
        specie.compute_max_fitness()


    # Print to file
    if passed:
        population.print_to_file(experiment_number, generation_number)

        vprint(1, f'Winner is organism number {winner_id}')
        organism.print_to_file(experiment_number)

    population.epoch(generation_number)

    if passed:
        return {
            'passed': True,
            'winner_id': winner_id,
            'winner_nodes': winner_nodes,
            'winner_genes': winner_genes
        }

    return {
        'passed': False
    }



def xor_evaluate(organism: Organism) -> bool:
    network: Network

    output_list: List[float] = []

    expected_output_list: List[float] = [0.0, 1.0, 1.0, 0.0]
    success_output_threshold: List[float] = [0.5, 0.5, 0.5, 0.5]

    # Check for successful activation
    success: bool

    # Used for figuring out how many nodes should be visited
    number_of_nodes: int

    # The maximum depth of the network
    network_depth: int

    input_list: List[List[float]] = [
        [1.0, 0.0, 0.0],
        [1.0, 0.0, 1.0],
        [1.0, 1.0, 0.0],
        [1.0, 1.0, 1.0]
    ]

    network = organism.network

    number_of_nodes = len(organism.genome.nodes)
    network_depth = network.maximum_depth()

    # Load and activate the network for each input
    for input in input_list:
        network.load_sensors(input)

        success = network.activate()

        for relax in range(network_depth + 1):
            success = network.activate()
            output = network.outputs[0].activation

        output_list.append(network.outputs[0].activation)

        network.flush()

    if success:
        errorsum = 0
        errorsum += abs(expected_output_list[0] - output_list[0])
        errorsum += abs(expected_output_list[1] - output_list[1])
        errorsum += abs(expected_output_list[2] - output_list[2])
        errorsum += abs(expected_output_list[3] - output_list[3])

        organism.fitness = (4.0 - errorsum) ** 2
        organism.error = errorsum

    else:
        # Flawed network
        errorsum = 999.0
        organism.fitness = 0.001

    vprint(3, f'Organism: {organism.genome.id}')
    vprint(3, f'Error: {output_list} -> {errorsum}')
    vprint(3, f'Fitness: {organism.fitness}')

    # Check if meets conditions
    if (
        abs(output_list[0] - expected_output_list[0]) <= success_output_threshold[0] and
        abs(output_list[1] - expected_output_list[1]) <= success_output_threshold[1] and
        abs(output_list[2] - expected_output_list[2]) <= success_output_threshold[2] and
        abs(output_list[3] - expected_output_list[3]) <= success_output_threshold[3]
    ):
        organism.winner = True
    else:
        organism.winner = False

    return organism.winner
