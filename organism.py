from typing import Dict

from genome import Genome

class Organism:

    def __init__(self, fit: int=None, genome: Genome=None, generation: int=None) -> Organism:
        # Initialize organism from fir, genome and generation number
        if fit and genome and generation:
            pass
