from yaml import load, Loader

from genome import Genome

verbosity: int = 0
numberOfTraitParameters: int = 8

def loadParameters(parameterFile: str) -> None:
    # Get global parameters

    # I don't know
    global linkTraitMutationSig
    global nodeTraitMutationSig


    # Mutation powers
    global traitMutationPower
    global weightMutationPower


    # Mutation probabilities
    global traitParameterMutationProbability
    global mutateOnlyProbability
    global mutateRandomTraitProbability
    global mutateLinkTraitProbability
    global mutateNodeTraitProbability
    global mutateLinkWeightsProbability
    global mutateToggleEnableProbability
    global mutateGeneReenableProbability
    global mutateAddNodeProbability
    global mutateAddLinkProbability


    # Coefficients
    global disjointCoefficient
    global excessCoefficient
    global mutationDifferenceCoefficient


    # Probabilities
    global recurrentProbability
    global recurrentOnlyProbability


    # Mating
    global interspeciesMateRate
    global mateMultipointAverageProbability
    global mateSinglepointProbability
    global mateOnlyProbability


    # Thresholds
    global compatibilityThreshold
    global survivalThreshold


    # Constants
    global ageSignificance
    global populationSize
    global dropoffAge
    global newLinkTries
    global printFrequency
    global babiesStolen
    global numberOfRuns
    global verbosity

    # Load parameters from file

    with open(parameterFile) as file:
        parameter = load(file, Loader=Loader)

        # Set parameters

        # I don't know
        linkTraitMutationSig = parameter['linkTraitMutationSig']
        nodeTraitMutationSig = parameter['nodeTraitMutationSig']


        # Mutation powers
        traitMutationPower = parameter['traitMutationPower']
        weightMutationPower = parameter['weightMutationPower']


        # Mutation probabilities
        traitParameterMutationProbability = parameter['traitParameterMutationProbability']
        mutateOnlyProbability = parameter['mutateOnlyProbability']
        mutateRandomTraitProbability = parameter['mutateRandomTraitProbability']
        mutateLinkTraitProbability = parameter['mutateLinkTraitProbability']
        mutateNodeTraitProbability = parameter['mutateNodeTraitProbability']
        mutateLinkWeightsProbability = parameter['mutateLinkWeightsProbability']
        mutateToggleEnableProbability = parameter['mutateToggleEnableProbability']
        mutateGeneReenableProbability = parameter['mutateGeneReenableProbability']
        mutateAddNodeProbability = parameter['mutateAddNodeProbability']
        mutateAddLinkProbability = parameter['mutateAddLinkProbability']


        # Coefficients
        disjointCoefficient = parameter['disjointCoefficient']
        excessCoefficient = parameter['excessCoefficient']
        mutationDifferenceCoefficient = parameter['mutationDifferenceCoefficient']


        # Probabilities
        recurrentProbability = parameter['recurrentProbability']
        recurrentOnlyProbability = parameter['recurrentOnlyProbability']


        # Mating
        interspeciesMateRate = parameter['interspeciesMateRate']
        mateMultipointAverageProbability = parameter['mateMultipointAverageProbability']
        mateSinglepointProbability = parameter['mateSinglepointProbability']
        mateOnlyProbability = parameter['mateOnlyProbability']


        # Thresholds
        compatibilityThreshold = parameter['compatibilityThreshold']
        survivalThreshold = parameter['survivalThreshold']


        # Constants
        ageSignificance = parameter['ageSignificance']
        populationSize = parameter['populationSize']
        dropoffAge = parameter['dropoffAge']
        newLinkTries = parameter['newLinkTries']
        printFrequency = parameter['printFrequency']
        babiesStolen = parameter['babiesStolen']
        numberOfRuns = parameter['numberOfRuns']
        verbosity = parameter['verbosity']
