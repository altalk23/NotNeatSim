from sys import argv
import neat
import experiments

def main():

    # Check for parameter file
    if len(argv) != 2:
        print('A parameters file (.yaml file) is required to run!')
        return -1

    # Load the parameters
    neat.load_parameters(argv[1])
    print(f'Loaded parameters from file {argv[1]}')

    print('Please choose an experiment:')
    print('1 - XOR')
    choice = input('Number: ')

    if choice == '1':
        population = experiments.xor_test(100)
    else:
        print('Not an option.')

    return 0



if __name__ == '__main__':
    main()
