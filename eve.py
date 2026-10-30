"""
demonstrating the eve attack. 
"""

from modular_math import modular_exponentiation

class Eve:

    def __init__(self):

        self.e1 = None
        self.e2 = None

        self.E1 = None
        self.E2 = None

    def create_public_values(
        self,
        p,
        g
    ):

        self.e1 = 3
        self.e2 = 7

        self.E1 = modular_exponentiation(
            g,
            self.e1,
            p
        )

        self.E2 = modular_exponentiation(
            g,
            self.e2,
            p
        )

        return self.E1, self.E2
