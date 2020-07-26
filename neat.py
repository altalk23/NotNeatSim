from random import uniform

from math import log, sqrt
from yaml import load, Loader

verbosity: int = 0
numberOfTraitParameters: int = 8
timeAliveMinimum: int = 0

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
    global mateMultipointProbability
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
        mateMultipointProbability = parameter['mateMultipointProbability']
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


iset = 0
def gaussrand():
    global gset, iset
    rsq = 0
    if iset == 0:
        while rsq == 0 or rsq >= 1:
            v1 = uniform(-1, 1)
            v2 = uniform(-1, 1)
            rsq = v1 ** 2 + v2 ** 2
        fac = sqrt(-2 * log(rsq) / rsq)
        gset = v1 * fac
        iset = 1
        return v2 * fac
    else:
        iset = 0
        return gset


# I don't know what in earth this is doing
def hebbian(weight, maxWeight, activeIn, activeOut, rates):
    hebbRate = rate[0]
    preRate = rate[1]
    postRate = rate[2]

    maxWeight = max(5, maxWeight)

    weight = min(max(weight, -maxWeight), maxWeight)

    negative = weight < 0
    weight = abs(weight)

    topWeight = min(weight + 2, maxWeight)

    if not negative:
        delta = (hebbRate * (maxWeight - weight) * activeIn * activeOut +
        preRate * topWeight  * activeIn * activeOut)
        return weight + delta
    else:
        # In the inhibatory case, we strengthen the synapse when output is low and input is high
        delta = (preRate * (maxWeight - weight) * activeIn * (1 - activeOut) -
        hebbRate * (topWeight + 2)  * activeIn * activeOut)
        return - weight - delta
