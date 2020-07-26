from __future__ import annotations

from random import random, uniform
from typing import Dict, List

import neat

class Trait:

    # Variable annotations
    id: int
    params: List[float]

    def __init__(self,
    id: int = None,
    params: List[float] = None,
    trait1: Trait = None,
    trait2: Trait = None,
    data: Dict[str, object] = None) -> None:

        # Construct a trait from parameters
        if (id is not None and
        params is not None):
            self.id = id
            self.params = params.copy()
            self.params[neat.numberOfTraitParameters - 1] = 0

        # Create a trait from averaging two traits:
        elif (trait1 is not None and
        trait2 is not None):
            self.id = trait1.id
            self.params = [(a + b) / 2 for a, b in zip(trait1.params, trait2.params)]

        # Generate the object from dict
        elif (data is not None):
            self.id = data['id']
            self.params = data['params']


    # Return the dict representation of the object
    def toDict(self) -> Dict[str, object]:
        data = {}

        data['id'] = self.id
        data['params'] = self.params

        return data


    # Perturb the trait parameters slightly
    def mutate(self) -> None:
        for i, v in enumerate(self.params):
            if random() > neat.traitParameterMutationProbability:
                v += uniform(-1, 1) * neat.traitMutationPower
                self.params[i] = min(max(v, 0), 1)
