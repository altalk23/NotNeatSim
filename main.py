from sys import argv

import experiments
import neat
from print import *

def main():

    # Check for parameter file
    if len(argv) != 2:
        vprint(0, 'A parameters file (.yaml file) is required to run!')
        return -1

    # Load the parameters
    neat.loadParameters(argv[1])
    vprint(1, f'Loaded parameters from file {argv[1]}')

    vprint(0, 'Please choose an experiment:')
    vprint(0, '1 - XOR')
    choice = '1' # input('Number: ')

    if choice == '1':
        population = experiments.xorTest(150)
    else:
        vprint(0, 'Not an option.')

    return 0



if __name__ == '__main__':
    main()
