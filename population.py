from typing import List
from math import ceil, floor
from random import randint

from yaml import dump

from genome import Genome
from organism import Organism
from mutator import Mutator
from specie import Specie
from print import vprint
import neat

class Population:

    # Variable annotations
    organisms: List[Organism] = []
    species: List[Specie] = []

    winner_genome: int
    highest_fitness: float
    highest_last_changed: int

    current_node_id: int
    current_innovation_number: int

    def __init__(self: Population, genome: Genome=None, size: Size=None) -> Population:
        # Initialize population from genome and size
        if genome and size:
            self.winner_genome = 0;
        	self.highest_fitness = 0.0;
        	self.highest_last_changed = 0;
        	self.spawn(genome, size);



    def spawn(self: Population, genome: Genome, size: int) -> None:

        # Variable annotations
        count: int
        new_genome: Genome
        new_organism: Organism

        # Create copies of the genome
        for count in range(1, size+1):
            new_genome = genome.duplicate(count)
            new_genome.mutate_link_weights(1.0, 1.0, Mutator.GAUSSIAN)
            new_genome.randomize_traits()

            new_organism = Organism(fit=0.0, genome=new_genome, generation=1);
            self.organisms.append(new_organism)

        # Store the current node id and innovation number
        self.current_node_id = new_genome.get_last_node_id()
        self.current_innovation_number = new_genome.get_last_innovation_number()

        # Split the population into species
        self.speciate()



    def speciate(self: Population) -> None:

        # Variable annotations
        compare_organism: Organism
        new_specie: Specie

        # Loop for each organism
        for organism in self.organisms:

            # Search for each specie
            for specie in self.species:
                compare_organism = specie[0]

                # Found compatible specie, add organism to specie
                if organism.genome.compatibility(compare_organism.genome) < neat.compatibility_threshold:
                    specie.add_organism(organism)
                    organism.specie = specie # TODO: move this to add_organism module
                    break

            # Didn't find a match, create new specie
            else:
                # Create the new specie
                new_specie = Specie(len(self.species) + 1)
                self.species.append(new_specie)
                new_specie.add_organism(organism)
                organism.specie = new_specie # TODO: move this to add_organism module



    def print_to_file(self: Population, experiment_number: int, generation_number: int) -> None:
        with open(f'output/Population #{experiment_number}.{generation_number}') as file:
            species = []

            # Add specie content
            for specie in self.species:
                species.append(specie.to_dict())

            # Write to file
            yaml.dump({
                'experiment_number': experiment_number,
                'generation_number': generation_number,
                'species': species
            }, file)



    def epoch(self: Population, generation: int) -> None:

        # Variable annotations

        # Fitness among all organisms
        total_fitness: int = 0
        average_fitness: int

        # Species sorted by maximum fitness
        sorted_species: List[Specie]

        # Specie constants
        target_number_of_species: int = 4;
        compatibility_mod: float = 0.3

        # Print the current generation
        vprint(2, f'Generation #{generation}:')


        # Sort the species by maximum fitness (using original fitness)
        sorted_species = sorted(self.species, key=lambda sp: sp.organisms[0].original_fitness, reverse=True)


        # Flag the lowest performing species over age 20 every 30 generations
        if generation % 30 == 0:
            for specie in reversed(sorted_species):
                if specie.age >= 20:
                    specie.obliterate = True
                    break

        vprint(2, f'Number of Species: {len(self.species)}')
        vprint(2, f'Compatibility Mod: {compatibility_mod}')


        # Adjust species' fitnesses using their ages
        for specie in self.species:
            specie.adjust_fitness()


        # TODO: Cleanup this code vv

        # Go through the organisms and add up their fitnesses to compute the overall average
        for organism in self.organisms:
            total_fitness += organism.fitness
        average_fitness = total_fitness / len(self.organisms)

        vprint(2, f'Overall Average Fitness: {average_fitness}')


        # TODO: Cleanup this code vv

        # Compute the expected number of offspring for each individual organism
        for organism in self.organisms:
            organism.expected_offspring = organism.fitness / average_fitness

        # Sort the species by maximum fitness (using original fitness)
        sorted_species = sorted(self.species, key=lambda sp: sp.organisms[0].original_fitness, reverse=True)

        # Now add those offspring up within each specie to get the number of offspring per specie
        precision_skim: float = 0.0
        total_offspring: int = 0
        for specie in sorted_species:
            precision_skim = specie.count_offsprint(precision_skim)
            total_offspring += specie.expected_offspring

        # If we lost precision, give an extra baby to the best Species
        if total_offspring < len(self.organisms):
            total_offspring += 1
            sorted_species[0].expected_offspring += 1

        # Achievement get: How Did We Get Here
        if total_offspring < len(self.organisms):
            for specie in self.species:
                if specie is best_specie:
                    specie.expected_offspring = len(self.organisms)
                else:
                    specie.expected_offspring = 0



        # Print out for debugging
        for specie in sorted_species:
            vprint(2, f'Specie #{specie.id}, Size {len(specie.organisms)}')
            vprint(2, f'Original fitness: {specie.organisms[0].original_fitness}')
            vprint(2, f'Last improved: {specie.age - specie.age_of_last_improvement}')


        # TODO: Cleanup this code vv

        # Check for Population-level stagnation
        sorted_species[0].organisms[0].population_champion = True
        if sorted_species[0].organisms[0].original_fitness > self.highest_fitness:
            self.highest_fitness = sorted_species[0].organisms[0].original_fitness
            self.highest_last_changed = 0
            vprint(2, f'New Population Record Fitness: {self.highest_fitness}')
        else:
            self.highest_last_changed += 1
            vprint(2, f'{self.highest_last_changed} generations since last population fitness record: {self.highest_fitness}')


        # TODO: Cleanup this code vv

        # Check for stagnation- if there is stagnation, perform delta-coding
        if highest_last_changed >= neat.dropoff_age + 5:
            vprint(3, f'Performing delta coding')
            self.highest_last_changed = 0


            if len(sorted_species) < 2:
                sorted_species[0].organisms[0].super_champion_offspring = neat.population_size
                sorted_species[0].expected_offspring = neat.population_size
                sorted_species[0].age_of_last_improvement = sorted_species[0].age
            else:
                for specie in sorted_species:
                    if specie is sorted_species[0]:
                        specie.organisms[0].super_champion_offspring = ceil(neat.population_size / 2)
                        specie.expected_offspring = ceil(neat.population_size / 2)
                        specie.age_of_last_improvement = specie.age

                    elif specie is sorted_species[1]:
                        specie.organisms[0].super_champion_offspring = floor(neat.population_size / 2)
                        specie.expected_offspring = floor(neat.population_size / 2)
                        specie.age_of_last_improvement = specie.age

                    else:
                        specie.expected_offspring = 0

        # TODO: Cleanup this code vv

        # STOLEN BABIES:  The system can take expected offspring away from
        # worse species and give them to superior species
        elif neat.babies_stolen > 0:

            # Take away a constant number of expected offspring from the worst few species
            stolen_babies = 0

            for specie in reversed(sorted_species):
                if specie.age > 5 and specie.expected_offspring > 2:
                    vprint(3, f'Stealing')

                    # Enough the finish the pool
                    if specie.expected_offspring > neat.babies_stolen - stolen_babies:
                        specie.expected_offspring -= neat.babies_stolen - stolen_babies
                        stolen_babies = neat.babies_stolen
                        break

                    # Not enough to finish the pool
                    else:
                        stolen_babies += specie.expected_offspring - 1
                        specie.expected_offspring = 1


            specie_iter = iter(sorted_species)

            try:
                # Skip dying species
                specie = next(specie_iter)
                while specie.last_improved() > neat.dropoff_age:
                    specie = next(specie_iter)

                # First specie
                if stolen_babies >= neat.babies_stolen // 5:
                    specie.organisms[0].super_champion_offspring += neat.babies_stolen // 5
                    specie.expected_offspring += neat.babies_stolen // 5
                    stolen_babies -= neat.babies_stolen // 5

                # Skip dying species
                specie = next(specie_iter)
                while specie.last_improved() > neat.dropoff_age:
                    specie = next(specie_iter)

                # Second specie
                if stolen_babies >= neat.babies_stolen // 5:
                    specie.organisms[0].super_champion_offspring += neat.babies_stolen // 5
                    specie.expected_offspring += neat.babies_stolen // 5
                    stolen_babies -= neat.babies_stolen // 5

                # Skip dying species
                specie = next(specie_iter)
                while specie.last_improved() > neat.dropoff_age:
                    specie = next(specie_iter)

                # Third specie
                if stolen_babies >= neat.babies_stolen // 10:
                    specie.organisms[0].super_champion_offspring += neat.babies_stolen // 10
                    specie.expected_offspring += neat.babies_stolen // 10
                    stolen_babies -= neat.babies_stolen // 10

                # Skip dying species
                specie = next(specie_iter)
                while specie.last_improved() > neat.dropoff_age:
                    specie = next(specie_iter)

                while stolen_babies > 0:
                    # Randomize a little

                    if randint(0, 9) > 0:
                        specie.organisms[0].super_champion_offspring += min(3, stolen_babies)
                        specie.expected_offspring += min(3, stolen_babies)
                        stolen_babies -= min(3, stolen_babies)

                    # Skip dying species
                    specie = next(specie_iter)
                    while specie.last_improved() > neat.dropoff_age:
                        specie = next(specie_iter)


            except StopIteration:

                # If any stolen babies aren't taken, give them to species #1's champ
                if stolen_babies > 0:
                    vprint(3, f'Not all given back, giving to best Species')

                    sorted_species[0].organisms[0].super_champion_offspring += stolen_babies
                    sorted_species[0].expected_offspring += stolen_babies
                    stolen_babies = 0


        # Kill of all organism marked for death
        organism_kill = reversed(list(enumerate(self.organism.copy())))
        for index, organism in organism_kill:
            if organism.eliminate:
                organism.specie.organisms.remove(organism)
                del self.organisms[index]


        # Perform reproduction. Reproduction is done on a per-specie basis.
        for specie in self.species.copy():
            specie.reproduce(generation, self, sorted_species)

        vprint(3, f'Reproduction Complete')

        # Destroy and remove the old generation from the organisms and species
        for organism in self.organisms:
            organism.specie.organisms.remove(organism)
        self.organisms = []

        # Remove all empty Species and age ones that survive
        organism_count = 0
        specie_kill = reversed(list(enumerate(self.species.copy())))
        for index, specie in specie_kill:
            # Remove the specie if empty
            if len(specie.organisms) < 1:
                del self.species[index]

            # Age any Species that is not newly created in this generation
            else:
                self.species[index].age += 1

                # Add them to the master list
                for organism in specie.organism:
                    organism.genome.id = organism_count
                    organism_count += 1
                    self.organisms.append(organism)


        # Epoch completed
        vprint(2, f'Epoch completed')



    def verify(self: Population) -> None:
        raise NotImplementedError



    def copy(self: Population, genome: Genome, size: int, power: float) -> None:
        raise NotImplementedError



    def rank_within_species(self: Population) -> None:
        raise NotImplementedError



    def estimate_all_averages(self: Population) -> None:
        raise NotImplementedError



    def choose_parent_specie(self: Population) -> Specie:
        raise NotImplementedError



    def remove_specie(self: Population, specie: Specie) -> None:
        raise NotImplementedError



    def remove_worst(self: Population) -> Organism:
        raise NotImplementedError



    def reproduce_champ(self: Population, generation: int) -> Organism:
        raise NotImplementedError



    def reassign_specie(self: Population, organism: Organism) -> None:
        raise NotImplementedError



    def switch_specie(self: Population, organism: Organism, original_specie: Specie, new_specie: Specie) -> None:
        raise NotImplementedError
