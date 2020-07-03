from sys import argv
import neat
import experiments
from print import vprint

def main():

    # Check for parameter file
    if len(argv) != 2:
        vprint(0, 'A parameters file (.yaml file) is required to run!')
        return -1

    # Load the parameters
    neat.load_parameters(argv[1])
    vprint(1, f'Loaded parameters from file {argv[1]}')

    vprint(0, 'Please choose an experiment:')
    vprint(0, '1 - XOR')
    choice = input('Number: ')

    if choice == '1':
        population = experiments.xor_test(100)
    else:
        vprint(0, 'Not an option.')

    return 0



if __name__ == '__main__':
    main()
