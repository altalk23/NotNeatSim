from yaml import load, Loader

def load_parameters(parameter_file: str) -> bool:
    # Get global parameters

    # I don't know
    global link_trait_mutation_sig
    global node_trait_mutation_sig


    # Mutation powers
    global trait_mutation_power
    global weight_mutation_power


    # Mutation probabilities
    global trait_parameter_mutation_probability
    global mutate_only_probability
    global mutate_random_trait_probability
    global mutate_link_trait_probability
    global mutate_node_trait_probability
    global mutate_link_weights_probability
    global mutate_toggle_enable_probability
    global mutate_gene_reenable_probability
    global mutate_add_node_probability
    global mutate_add_link_probability


    # Coefficients
    global disjoint_coefficient
    global excess_coefficient
    global mutation_difference_coefficient


    # Probabilities
    global recurse_probability
    global recurse_only_probability


    # Mating
    global interspecies_mate_rate
    global mate_multipoint_average_probability
    global mate_singlepoint_probability
    global mate_only_probability


    # Thresholds
    global compatibility_threshold
    global survival_threshold


    # Constants
    global age_significance
    global population_size
    global dropoff_age
    global new_link_tries
    global print_frequency
    global babies_stolen
    global number_of_runs
    global verbosity

    # Load parameters from file

    with open(parameter_file) as file:
        parameter = load(file, Loader=Loader)

        # Set parameters

        # I don't know
        link_trait_mutation_sig = parameter['link_trait_mutation_sig']
        node_trait_mutation_sig = parameter['node_trait_mutation_sig']


        # Mutation powers
        trait_mutation_power = parameter['trait_mutation_power']
        weight_mutation_power = parameter['weight_mutation_power']


        # Mutation probabilities
        trait_parameter_mutation_probability = parameter['trait_parameter_mutation_probability']
        mutate_only_probability = parameter['mutate_only_probability']
        mutate_random_trait_probability = parameter['mutate_random_trait_probability']
        mutate_link_trait_probability = parameter['mutate_link_trait_probability']
        mutate_node_trait_probability = parameter['mutate_node_trait_probability']
        mutate_link_weights_probability = parameter['mutate_link_weights_probability']
        mutate_toggle_enable_probability = parameter['mutate_toggle_enable_probability']
        mutate_gene_reenable_probability = parameter['mutate_gene_reenable_probability']
        mutate_add_node_probability = parameter['mutate_add_node_probability']
        mutate_add_link_probability = parameter['mutate_add_link_probability']


        # Coefficients
        disjoint_coefficient = parameter['disjoint_coefficient']
        excess_coefficient = parameter['excess_coefficient']
        mutation_difference_coefficient = parameter['mutation_difference_coefficient']


        # Probabilities
        recurse_probability = parameter['recurse_probability']
        recurse_only_probability = parameter['recurse_only_probability']


        # Mating
        interspecies_mate_rate = parameter['interspecies_mate_rate']
        mate_multipoint_average_probability = parameter['mate_multipoint_average_probability']
        mate_singlepoint_probability = parameter['mate_singlepoint_probability']
        mate_only_probability = parameter['mate_only_probability']


        # Thresholds
        compatibility_threshold = parameter['compatibility_threshold']
        survival_threshold = parameter['survival_threshold']


        # Constants
        age_significance = parameter['age_significance']
        population_size = parameter['population_size']
        dropoff_age = parameter['dropoff_age']
        new_link_tries = parameter['new_link_tries']
        print_frequency = parameter['print_frequency']
        babies_stolen = parameter['babies_stolen']
        number_of_runs = parameter['number_of_runs']
        verbosity = parameter['verbosity']

        return True
