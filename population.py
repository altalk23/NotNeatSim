from typing import List

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
        total_fitness: int
        average_fitness: int

        # Species sorted by maximum fitness
        sorted_species: List[Specie]

        # Sort the species by maximum fitness (using original fitness)
        sorted_species = sorted(self.species, key=lambda sp: sp.organisms[0].original_fitness, reverse=True)
        best_specie = sorted_species[0]

        for specie in sorted_species:
            vprint(2, f'Specie #{specie.id}, Size {len(specie.organisms)}')
            vprint(2, f'Original fitness: {specie.organisms[0].original_fitness}')
            vprint(2, f'Last improved: {specie.age - specie.age_of_last_improvement}')



    def verify(self: Population) -> None:
        pass
