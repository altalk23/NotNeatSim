from __future__ import annotations

from copy import deepcopy
from random import choice, random, uniform
from typing import Dict, List

from gene import *
from mutator import *
from network import *
from node import *
from nodeplace import *
from population import *
from print import *
from trait import *
import neat

class Genome:

    # Variable annotations
    id: int

    traits: List[Trait]
    genes: List[Gene]
    nodes: List[Node]

    phenotype: Network = None


    def __init__(self,
    id: int = None,
    traits: List[Trait] = None,
    genes: List[Gene] = None,
    nodes: List[Node] = None,
    links: List[Link] = None,
    inum: int = None,
    hnum: int = None,
    onum: int = None,
    hmax: int = None,
    recurrent: bool = None,
    linkProbability: float = None,
    type: int = None,
    data: Dict[str, object] = None) -> None:

        self.traits = []
        self.genes = []
        self.nodes = []

        # This special constructor creates a Genome...
        if (id is not None and
        inum is not None and
        hnum is not None and
        onum is not None and
        hmax is not None and
        recurrent is not None and
        linkProbability is not None):
            raise NotImplementedError

        # Special constructor that creates a Genome of 3 possible types
        elif (type is not None and
        inum is not None and
        hnum is not None and
        onum is not None):
            raise NotImplementedError

        # Constructor which takes full genome specs and puts them into the new one
        elif (id is not None and
        traits is not None and
        nodes is not None and
        genes is not None):

            self.id = id
            self.traits = traits
            self.genes = genes
            self.nodes = nodes

        # Constructor which takes in links (not genes) and creates a Genome
        elif (id is not None and
        traits is not None and
        nodes is not None and
        links is not None):
            raise NotImplementedError

        # Generate the object from dict
        elif (data is not None):
            self.id = data['id']

            self.traits = [Trait(data=d) for d in data['traits']]
            self.nodes = [Node(data=d, traits=self.traits) for d in data['nodes']]
            self.genes = [Gene(data=d, traits=self.traits, nodes=self.nodes) for d in data['genes']]


    # Loads a new Genome from a file
    def newGenomeLoad(self, filename: str) -> Genome:
        raise NotImplementedError


    # Generate a network phenotype from this Genome with specified id
    def genesis(self, id: int) -> Newtork:

        inputList: List[Node] = []
        outputList: List[Node] = []
        allList: List[Node] = []

        inode: Node
        onode: Node

        newNode: Node
        newLink: Link
        newNet: Network

        maxWeight: float = 0

        # Create the nodes
        for node in self.nodes:
            newNode = Node(type=node.type, id=node.id)

            newNode.deriveTrait(node.trait)

            # Check for input or output designation of node
            if node.place is NodePlace.INPUT:
                inputList.append(newNode)
            elif node.place is NodePlace.BIAS:
                inputList.append(newNode)
            elif node.place is NodePlace.OUTPUT:
                outputList.append(newNode)

            # Keep track of all nodes, not just input and output
            allList.append(newNode)

            # Have the node specifier point to the node it generated
            node.analogue = newNode

        # Create the links by iterating through the genes
        for gene in self.genes:
            # Only create the link if the gene is enabled
            if gene.enable:
                inode = gene.link.inode.analogue
                onode = gene.link.onode.analogue

                # NOTE: This line could be run through a recurrency check if desired
                newLink = Link(weight=gene.link.weight, inode=inode, onode=onode, recurrent=gene.link.recurrent)
                onode.incoming.append(newLink)
                inode.outcoming.append(newLink)

                # Derive link's parameters from its Trait pointer
                newLink.deriveTrait(gene.link.trait)

                # Keep track of maximum weight
                maxWeight = max(maxWeight, abs(newLink.weight))

        # Create the new network
        newNet = Network(inputs=inputList, outputs=outputList, allnodes=allList, id=id)

        # Attach genotype and phenotype together
        newNet.genotype = self
        self.phenotype = newNet

        newNet.maxWeight = maxWeight

        return newNet


    # For debugging: A number of tests can be run on a genome to check its integrity
    def verify(self) -> bool:
        raise NotImplementedError


    # Dump this genome to specified file
    def printToFile(self, filename: str) -> None:
        raise NotImplementedError


    # Dump this genome to a dict object
    def toDict(self) -> Dict[str, object]:
        data = {}

        data['id'] = self.id

        data['traits'] = [trait.toDict() for trait in self.traits]
        data['genes'] = [gene.toDict() for gene in self.genes]
        data['nodes'] = [node.toDict() for node in self.nodes]

        return data


    # Duplicate this Genome to create a new one with the specified id
    def duplicate(self, id: int) -> Genome:
        #print(f"duplicated with {id}")
        genome = deepcopy(self)
        genome.id = id
        return genome


    # Return id of final Node in Genome
    def getLastNodeId(self) -> int:
        return self.nodes[-1].id + 1


    # Return last innovation number in Genome
    def getLastInnovationNumber(self) -> double:
        return self.genes[-1].innovation + 1


    # Perturb params in one trait
    def mutateRandomTrait(self) -> None:
        choice(self.traits).mutate()


    # Change random link's trait. Repeat count times
    def mutateLinkTrait(self, count: int) -> None:
        for index in range(count):
            gene = choice(self.genes)
            trait = choice(self.traits)
            gene.link.trait = trait


    # Change random node's trait count times
    def mutateNodeTrait(self, count: int) -> None:
        for index in range(count):
            node = choice(self.nodes)
            trait = choice(self.traits)
            node.trait = trait


    # Add Gaussian noise to linkweights either GAUSSIAN or UNIFORM (from zero)
    def mutateLinkWeights(self, power: float, rate: float, mutationType: Mutator) -> None:

        # Once in a while really shake things up
        severe: bool = False

        if random() > 0.5:
            severe = True

        num = 0
        # Loop on all genes
        for gene in self.genes:
            # Don't mutate weights of frozen links
            if not gene.frozen:

                # For severe ones
                if severe:
                    gausspoint = 0.3
                    coldgausspoint = 0.2

                # For last genes
                elif len(self.genes) >= 10 and num > len(self.genes) * 0.8:
                    gausspoint = 0.5
                    coldgausspoint = 0.2

                else:
                    # Half the time don't do any cold mutations
                    if random() > 0.5:
                        gausspoint = 1 - rate
                        coldgausspoint = 0.1
                    else:
                        gausspoint = 1 - rate
                        coldgausspoint = 0

                randnum = uniform(-1, 1) * power

                if mutationType is Mutator.GAUSSIAN:
                    if random() > gausspoint:
                        gene.link.weight += randnum
                    elif random() > coldgausspoint:
                        gene.link.weight = randnum
                elif mutationType is Mutator.COLDGAUSSIAN:
                    gene.link.weight = randnum

                gene.link.weight = min(max(gene.link.weight, -8), 8)

                gene.mutation = gene.link.weight

                num += 1


    # Toggle genes on or off
    def mutateToggleEnable(self, count: int) -> None:
        raise NotImplementedError


    # Find first disabled gene and enable it
    def mutateGeneReenable(self) -> None:
        raise NotImplementedError


    # Mutate genome by adding a node respresentation
    def mutateAddNode(self, population: Population) -> None:

        gene: Gene # The random gene
        link: Link # Gene's link
        inode: Node # Link's in node
        onode: Node # Link's out node

        weight: float # Link's weight
        trait: Trait # Link's trait

        newNode: Node # Create the new Node
        newGene1: Gene
        newGene2: Gene

        # Alternative random gaussian choice of genes NOT USED in this
        for _ in range(20):
            gene = choice(self.genes)
            if gene.enable and gene.link.inode.place is not NodePlace.BIAS:
                break
        else:
            # If we couldn't find anything so say goodbye
            return

        # Disabled the gene
        gene.enable = False

        # Extract the link
        link = gene.link
        inode = link.inode
        onode = link.onode
        weight = link.weight
        trait = link.trait


        for innovation in population.innovations:
            if (innovation.type is InnovationType.NEWNODE and
            innovation.inode == inode.id and
            innovation.onode == onode.id and
            innovation.oldNum == gene.innovation):
            # Here, the innovation has been done before

                # Create the new node
                newNode = Node(type=NodeType.NEURON, id=innovation.newNode, place=NodePlace.HIDDEN)
                newNode.trait = self.traits[0]

                # Create the new Genes
                newGene1 = Gene(trait=trait, weight=1, inode=inode, onode=newNode, recurrent=link.recurrent, innovation=innovation.num1, mutation=0)
                newGene2 = Gene(trait=trait, weight=1, inode=newNode, onode=onode, recurrent=False, innovation=innovation.num2, mutation=0)

                break

        else:
            # The innovation is totally novel

            # Create the new node
            newNode = Node(type=NodeType.NEURON, id=population.currentNodeId, place=NodePlace.HIDDEN)
            newNode.trait = self.traits[0]
            population.currentNodeId += 1

            # Create the new Genes
            newGene1 = Gene(trait=trait, weight=1, inode=inode, onode=newNode, recurrent=link.recurrent, innovation=population.currentInnovationNumber, mutation=0)
            newGene2 = Gene(trait=trait, weight=1, inode=newNode, onode=onode, recurrent=False, innovation=population.currentInnovationNumber + 1, mutation=0)

            population.innovations.append(Innovation(
                inode=inode.id,
                onode=onode.id,
                num1=population.currentInnovationNumber,
                num2=population.currentInnovationNumber+1,
                newNode=newNode.id,
                oldNum=gene.innovation))
            population.currentInnovationNumber += 2

        self.addGene(newGene1)
        self.addGene(newGene2)
        self.insertNode(self.nodes, newNode)


    """
    CODED BY BIRKIY
    fixed
    I guess
    """
    # Mutate the genome by adding a new link between 2 random nodes
    def mutateAddLink(self, population: Population, tries: int) -> None:
        nodeCount: int # Counter for finding nodes
        node1: Node # Pointers to the nodes
        node2: Node # Pointers to the nodes
        found: bool = False # Tells whether an open pair was found

        isRecurrent: bool # Indicates whether proposed link is recurrent
        newGene: Gene # The new gene

        trait: Trait # Random trait finder

        newWeight: float # The new weight for the new link

        done: bool
        recurrent: bool = False
        loopRecurrent: bool
        firstNonSensorIndex: int = 0

        # These are used to avoid getting stuck in an infinite loop checking
    	# for recursion
        # Note that we check for recursion to control the frequency of
    	# adding recurrent links rather than to prevent any paricular
    	# kind of error

        thresh: int = len(self.nodes)**2
        count: int = 0

        # Make attempts to find an unconnected pair
        tryCount = 0

        # Decide whether to make this recurrent
        if random() < neat.recurrentOnlyProbability:
            recurrent = True

        # Find the first non-sensor so that the to-node won't look at sensors as
    	# possible destinations
        firstNonSensorIndex = 0
        for index, node in enumerate(self.nodes):
            if node.type is not NodeType.SENSOR:
                firstNonSensorIndex = index
                break

        # Here is the recurrent finder loop- it is done separately
        if recurrent:
            while tryCount < tries:
                # Some of the time try to make a recurrent loop
                if random() > 0.5:
                    loopRecurrent = True
                else:
                    loopRecurrent = False

                if loopRecurrent:
                    node1 = choice(self.nodes[firstNonSensorIndex:])
                    node2 = node1
                else:
                    # Choose random node
                    node1 = choice(self.nodes)
                    node2 = choice(self.nodes[firstNonSensorIndex:])


                # See if a recurrent link already exists  ALSO STOP AT END OF GENES!!!!
                for gene in self.genes:

                    if not (nodep2.type is not NodeType.SENSOR and # Don't allow SENSORS to get input
                    not gene.link.inode is node1 and
                    gene.link.onode is node2 and
                    gene.link.recurrent):
                        # Didn't make to the end of genes

                        tryCount += 1
                        break

                else:
                    # Made to the end of genes

                    count = 0
                    isRecurrent = self.phenotype.isRecurrent(node1.analogue, node2.analogue, count, thresh)

                    # ADDED: CONSIDER connections out of outputs recurrent
                    if (
                    node1.type == NodeType.OUTPUT or
                    node2.type == NodeType.OUTPUT
                    ):
                        isRecurrent = True

                    # Make sure it finds the right kind of link (recur)
                    if not isRecurrent:
                        tryCount += 1
                    else:
                        tryCount = tries
                        found = True


        else:
            # Loop to find a nonrecurrent link
            while tryCount < tries:

                # Chose random nodes
                node1 = choice(self.nodes)
                node2 = choice(self.nodes[firstNonSensorIndex:])

                # See if a recurrent link already exists  ALSO STOP AT END OF GENES!!!!
                for gene in self.genes:

                    if not (node2.type is not NodeType.SENSOR and # Don't allow SENSORS to get input
                    not gene.link.inode is node1 and
                    gene.link.onode is node2 and
                    gene.link.recurrent):
                        # Didn't make to the end of genes

                        tryCount += 1
                        break

                else:
                    # Made to the end of genes

                    count = 0
                    isRecurrent = self.phenotype.isRecurrent(node1.analogue, node2.analogue, count, thresh)

                    # ADDED: CONSIDER connections out of outputs recurrent
                    if (
                    node1.type == NodeType.OUTPUT or
                    node2.type == NodeType.OUTPUT
                    ):
                        isRecurrent = True

                    # Make sure it finds the right kind of link (recur)
                    if not isRecurrent:
                        tryCount += 1
                    else:
                        tryCount = tries
                        found = True

            # End of normal link finding loop

        if found:

            # If it was supposed to be recurrent, make sure it gets labeled that way
            if recurrent:
                isRecurrent = True
            vprint(3, 'found')
            # loop to find a non recurrent link
            for innovation in innovations:

                # Match the innovation in the innovs list
                if (innovation.type is InnovationType.NEWLINK and
                innovation.inode == node1.id and
                innovation.onode == node2.id and
                innovation.recurrent == isRecurrent):

                    # Create the new gene
                    newGene = Gene(
                        trait=trait,
                        weight=newWeight,
                        inode=node1,
                        onode=node2,
                        recurrent=isRecurrent,
                        innovation=population.currentInnovationNumber,
                        mutation=newWeight
                    )

                    break
            # The innovation is totally novel
            else:
                # If the phenotype does not exist, exit
                if phenotype == 0:
                    vprint(1, 'Error: Attempt to add link to genome with no phenotype')
                    return None

                # Choose a random trait
                trait = choice(self.traits)

                # Choose the new weight
                newWeight = uniform(-1, 1)

                # Create the new gene
                newGene = Gene(
                    trait=trait,
                    weight=newWeight,
                    inode=node1,
                    onode=node2,
                    recurrent=isRecurrent,
                    innovation=population.currentInnovationNumber,
                    mutation=newWeight
                )

                # Add the innovation
                population.innovations.append(Innovation(
                    inode=node1.id,
                    onode=node2.id,
                    num1=population.currentInnovationNumber,
                    weight=newWeight,
                    trait=trait
                ))

                population.currentInnovationNumber += 1



            self.addGene(newGene)


    # Mutate genome by adding a sensor node
    def mutateAddSensor(self, innovations: List[Innovation], currentInnovationNumber: int) -> None:
        raise NotImplementedError


    # Adds a new gene that has been created through a mutation
    def addGene(self, gene: Gene) -> None:
        try:
            index = next(i for i, g in enumerate(self.genes) if g.innovation >= gene.innovation)
            self.genes.insert(index, gene)
        except StopIteration:
            self.genes.append(gene)


    # Inserts a Node into a given ordered list of Nodes in order
    def insertNode(self, nodelist: List[Node], node: Node) -> None:
        #print(node.id, node.type, node.place)
        try:
            index = next(i for i, n in enumerate(nodelist) if n.id >= node.id)
            nodelist.insert(index, node)
        except StopIteration:
            nodelist.append(node)


    # This method mates this Genome with another genome.
    def mateMultipoint(self, genome: Genome, genomeId: int, fitness1: float, fitness2: float, outside: bool) -> Genome:
        # Moving through the two parents' traits
        trait1: Trait
        trait2: Trait

        # Moving through the two parents' genes
        i1: int = 0
        i2: int = 0
        chosenGene: Gene

        # Tells if the first genome (this one) has better fitness or not
        better: bool

        # The baby Genome will contain these new Traits, NNodes, and Genes
        newTraits: List[Trait] = []
        newNodes: List[Node] = []
        newGenes: List[Gene] = []

        # Trait number for a node
        traitNumber: int

        newINode: Node
        newONode: Node

        #print("mate")
        #self.print()
        #genome.print()

        # First, average the Traits from the 2 parents to form the baby's Traits
        trait2 = genome.traits[0]
        for trait1 in self.traits:
            newTraits.append(Trait(trait1=trait1, trait2=trait2))

        # Figure out which genome is better
        better = fitness1 > fitness2 or len(self.genes) < len(genome.genes)

        # Make sure all sensors and outputs are included
        for node in genome.nodes:
            if (node.place is NodePlace.INPUT or
            node.place is NodePlace.BIAS or
            node.place is NodePlace.OUTPUT):
                if node.trait is not None:
                    traitNumber = 0
                else:
                    traitNumber = node.trait.id - self.traits[0].id

                # Create a new node off the sensor or output
                newONode = Node(node=node, trait=newTraits[traitNumber])
                self.insertNode(newNodes, newONode)


        # Now move through the Genes of each parent until both genomes end
        while i1 < len(self.genes) or i2 < len(genome.genes):
            # Default to not skipping a chosen gene
            skip = False

            if i1 == len(self.genes):
                chosenGene = genome.genes[i2]
                i2 += 1
                if better: skip = True

            elif i2 == len(genome.genes):
                chosenGene = self.genes[i1]
                i1 += 1
                if not better: skip = True

            else:
                innovation1 = self.genes[i1].innovation
                innovation2 = genome.genes[i2].innovation

                if innovation1 == innovation2:
                    chosenGene = choice([self.genes[i1], genome.genes[i2]])

                    # If one is disabled, the corresponding gene in the offspring will likely be disabled
                    disable = False
                    if not self.genes[i1].enable or not genome.genes[i2].enable:
                        if random() < 0.75: disable = True

                    i1 += 1
                    i2 += 1

                elif innovation1 < innovation2:
                    chosenGene = self.genes[i1]
                    i1 += 1
                    if not better: skip = True

                elif innovation2 < innovation1:
                    chosenGene = genome.genes[i2]
                    i2 += 1
                    if better: skip = True


            # Check to see if the chosengene conflicts with an already chosen gene
            for chosenGene2 in newGenes:
                if chosenGene2.link == chosenGene.link:
                    skip = True

            #print(chosenGene.link.inode.id, chosenGene.link.onode.id, "ids", skip, "skip")

            # Now add the chosengene to the baby
            if not skip:

                # Get the trait pointer
                if chosenGene.link.trait == None:
                    traitNumber = self.traits[0].id - 1
                else:
                    traitNumber = chosenGene.link.trait.id - self.traits[0].id # The subtracted number normalizes depending on whether traits start counting at 1 or 0

                # Next check for the nodes, add them if not in the baby Genome already
                inode = chosenGene.link.inode

                onode = chosenGene.link.onode

                # Check for inode in the newnodes list
                if inode.id < onode.id:

                    # Checking for inode's existence
                    for node in newNodes:
                        if node.id == inode.id:
                            newINode = node
                            break
                    else:
                        # Here we know the node doesn't exist so we have to add it
                        if inode.trait is None:
                            nodeTraitNumber = 0
                        else:
                            nodeTraitNumber = inode.trait.id - self.traits[0].id

                        newINode = Node(node=inode, trait=newTraits[nodeTraitNumber])
                        self.insertNode(newNodes, newINode)

                # Checking for onode's existence
                for node in newNodes:
                    if node.id == onode.id:
                        newONode = node
                        break
                else:
                    # Here we know the node doesn't exist so we have to add it
                    if inode.trait is None:
                        nodeTraitNumber = 0
                    else:
                        nodeTraitNumber = onode.trait.id - self.traits[0].id

                    newONode = Node(node=onode, trait=newTraits[nodeTraitNumber])
                    self.insertNode(newNodes, newONode)

                # If the onode has a higher id than the inode we want to add it first
                if onode.id < inode.id:

                    # Checking for inode's existence
                    for node in newNodes:
                        if node.id == inode.id:
                            newINode = node
                            break
                    else:
                        # Here we know the node doesn't exist so we have to add it
                        if inode.trait is None:
                            nodeTraitNumber = 0
                        else:
                            nodeTraitNumber = inode.trait.id - self.traits[0].id

                        newINode = Node(node=inode, trait=newTraits[nodeTraitNumber])
                        self.insertNode(newNodes, newINode)


                # Add the Gene
                newGene = Gene(gene=chosenGene, trait=newTraits[traitNumber], inode=newINode, onode=newONode)

                if disable:
                    newGene.enable = False
                    disable = False

                newGenes.append(newGene)

        newGenome = Genome(id=genomeId, traits=newTraits, nodes=newNodes, genes=newGenes)


        #print("mate end")
        #self.print()
        #genome.print()
        #newGenome.print()
        return newGenome


    # This method mates like multipoint but instead of selecting one it averages their weights
    def mateMultipointAverage(self, genome: Genome, genomeId: int, fitness1: float, fitness2: float, outside: bool) -> Genome:
        # Moving through the two parents' traits
        trait1: Trait
        trait2: Trait

        # Moving through the two parents' genes
        i1: int = 0
        i2: int = 0
        chosenGene: Gene

        # Tells if the first genome (this one) has better fitness or not
        better: bool

        # The baby Genome will contain these new Traits, NNodes, and Genes
        newTraits: List[Trait] = []
        newNodes: List[Node] = []
        newGenes: List[Gene] = []

        # Trait number for a node
        traitNumber: int

        newINode: Node
        newONode: Node

        # First, average the Traits from the 2 parents to form the baby's Traits
        trait2 = genome.traits[0]
        for trait1 in self.traits:
            newTraits.append(Trait(trait1=trait1, trait2=trait2))

        # Figure out which genome is better
        better = fitness1 > fitness2 or len(self.genes) < len(genome.genes)

        # Make sure all sensors and outputs are included
        for node in genome.nodes:
            if (node.place is NodePlace.INPUT or
            node.place is NodePlace.BIAS or
            node.place is NodePlace.OUTPUT):
                if node.trait is not None:
                    traitNumber = 0
                else:
                    traitNumber = node.trait.id - self.traits[0].id

                # Create a new node off the sensor or output
                newONode = Node(node=node, trait=newTraits[traitNumber])
                self.insertNode(newNodes, newONode)


        # Now move through the Genes of each parent until both genomes end
        while i1 < len(self.genes) or i2 < len(genome.genes):
            # Default to not skipping a chosen gene
            skip = False

            if i1 == len(self.genes):
                chosenGene = genome.genes[i2]
                i2 += 1
                if better: skip = True

            elif i2 == len(genome.genes):
                chosenGene = self.genes[i1]
                i1 += 1
                if not better: skip = True

            else:
                innovation1 = self.genes[i1].innovation
                innovation2 = genome.genes[i2].innovation

                if innovation1 == innovation2:
                    # Average them into the avgene
                    averageGene = Gene()
                    averageGene.link.trait = choice([self.genes[i1].link.trait, genome.genes[i2].link.trait])

                    # WEIGHTS AVERAGED HERE
                    averageGene.link.weight = (self.genes[i1].link.weight + genome.genes[i2].link.weight) / 2

                    averageGene.link.inode = choice([self.genes[i1].link.inode, genome.genes[i2].link.inode])
                    averageGene.link.onode = choice([self.genes[i1].link.onode, genome.genes[i2].link.onode])
                    averageGene.link.recurrent = choice([self.genes[i1].link.recurrent, genome.genes[i2].link.recurrent])

                    averageGene.innovation = self.genes[i1].innovation
                    averageGene.mutation = (self.genes[i1].mutation + genome.genes[i2].mutation) / 2

                    averageGene.frozen = False

                    # If one is disabled, the corresponding gene in the offspring will likely be disabled
                    averageGene.enable = True
                    if not self.genes[i1].enable or not genome.genes[i2].enable:
                        if random() < 0.75: averageGene.enable = False

                    chosenGene = averageGene

                    i1 += 1
                    i2 += 1

                elif innovation1 < innovation2:
                    chosenGene = self.genes[i1]
                    i1 += 1
                    if not better: skip = True

                elif innovation2 < innovation1:
                    chosenGene = genome.genes[i2]
                    i2 += 1
                    if better: skip = True


            # Check to see if the chosengene conflicts with an already chosen gene
            for chosenGene2 in newGenes:
                if chosenGene2.link == chosenGene.link:
                    skip = True
                    
            # Now add the chosengene to the baby
            if not skip:

                # Get the trait pointer
                if chosenGene.link.trait == None:
                    traitNumber = self.traits[0].id - 1
                else:
                    traitNumber = chosenGene.link.trait.id - self.traits[0].id # The subtracted number normalizes depending on whether traits start counting at 1 or 0

                # Next check for the nodes, add them if not in the baby Genome already
                inode = chosenGene.link.inode
                onode = chosenGene.link.onode

                # Check for inode in the newnodes list
                if inode.id < onode.id:

                    # Checking for inode's existence
                    for node in newNodes:
                        if node.id == inode.id:
                            newINode = node
                            break
                    else:
                        # Here we know the node doesn't exist so we have to add it
                        if inode.trait is None:
                            nodeTraitNumber = 0
                        else:
                            nodeTraitNumber = inode.trait.id - self.traits[0].id

                        newINode = Node(node=inode, trait=newTraits[nodeTraitNumber])
                        self.insertNode(newNodes, newINode)

                # Checking for onode's existence
                for node in newNodes:
                    if node.id == onode.id:
                        newONode = node
                        break
                else:
                    # Here we know the node doesn't exist so we have to add it
                    if inode.trait is None:
                        nodeTraitNumber = 0
                    else:
                        nodeTraitNumber = onode.trait.id - self.traits[0].id

                    newONode = Node(node=onode, trait=newTraits[nodeTraitNumber])
                    self.insertNode(newNodes, newONode)

                # If the onode has a higher id than the inode we want to add it first
                if onode.id < inode.id:

                    # Checking for inode's existence
                    for node in newNodes:
                        if node.id == inode.id:
                            newINode = node
                            break
                    else:
                        # Here we know the node doesn't exist so we have to add it
                        if inode.trait is None:
                            nodeTraitNumber = 0
                        else:
                            nodeTraitNumber = inode.trait.id - self.traits[0].id

                        newINode = Node(node=inode, trait=newTraits[nodeTraitNumber])
                        self.insertNode(newNodes, newINode)


                # Add the Gene
                newGene = Gene(gene=chosenGene, trait=newTraits[traitNumber], inode=newINode, onode=newONode)

                newGenes.append(newGene)

        newGenome = Genome(id=genomeId, traits=newTraits, nodes=newNodes, genes=newGenes)
        return newGenome


    # This method is similar to a standard single point CROSSOVER operator.
    def mateSinglepoint(self, genome: Genome) -> Genome:
        raise NotImplementedError


    # This function gives a measure of compatibility between two Genomes
    def compatibility(self, genome: Genome) -> float:

        maxSize = max(len(self.genes), len(genome.genes))
        excess = 0
        matching = 0
        disjoint = 0
        mutationDifference = 0

        i1 = 0
        i2 = 0
        while i1 < len(self.genes) or i2 < len(genome.genes):
            if i1 == len(self.genes):
                i2 += 1
                excess += 1
            elif i2 == len(genome.genes):
                i1 += 1
                excess += 1
            else:
                gene1 = self.genes[i1]
                gene2 = genome.genes[i2]

                if gene1.innovation == gene2.innovation:
                    matching += 1
                    mutationDifference += abs(gene1.mutation - gene2.mutation)
                    i1 += 1
                    i2 += 1

                elif gene1.innovation > gene2.innovation:
                    disjoint += 1
                    i2 += 1

                elif gene1.innovation < gene2.innovation:
                    disjoint += 1
                    i1 += 1

        return (neat.disjointCoefficient * disjoint +
        neat.excessCoefficient * excess +
        neat.mutationDifferenceCoefficient * mutationDifference / matching)


    # This function compares two traits named trait1 and trait2
    def compareTrait(self, trait1: Trait, trait2: Trait) -> float:
        raise NotImplementedError


    # Return number of non-disabled genes
    def extrons(self) -> int:
        return sum(1 for gene in self.genes if gene.enable)


    # Randomize the trait pointers of all the node and connection genes
    def randomizeTraits(self) -> None:

        # Go through all nodes and randomize their trait pointers
        for node in self.nodes:
            trait = choice(self.traits)
            node.trait = trait

        # Go through all connections and randomize their trait pointers
        for gene in self.genes:
            trait = choice(self.traits)
            gene.link.trait = trait


    def print(self):
        genomeDict = self.toDict()
        _id = genomeDict['id']
        _traits = genomeDict['traits']
        _nodes = genomeDict['nodes']
        _genes = genomeDict['genes']
        _traitprint = ''.join([f'Trait #{trait["id"]} {trait["params"]}\n' for trait in _traits])
        _nodeprint = ''.join([f'Node #{node["id"]}\n' for node in _nodes])
        _geneprint = ''.join([f'Node #{gene["input"]} ————{gene["weight"]}————> Node #{gene["output"]}\n' for gene in _genes])
        vprint(1, f'Genome ID: {_id}')
        vprint(1, f'Genome traits: {_traitprint}')
        vprint(1, f'Genome nodes: {_nodeprint}')
        vprint(1, f'Genome genes: {_geneprint}')
