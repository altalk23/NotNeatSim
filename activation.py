from math import *

class Activation:

    def sigmoid(self, input):
        return 1/(1+exp(-input * 4.924273)) # 4.924273 is slope
