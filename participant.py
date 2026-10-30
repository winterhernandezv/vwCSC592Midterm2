"""
represents a participant.
"""

import secrets

from modular_math import modular_exponentiation

class Participant:

    def __init__(self, name):

        self.name = name

        self.private_exponent = None
        self.public_value = None
        self.shared_secret = None

    def generate_private_exponent(self, p):

        self.private_exponent = (
            secrets.randbelow(p - 3) + 2
        )

        return self.private_exponent

    def generate_public_value(self, g, p):

        self.public_value = modular_exponentiation(
            g,
            self.private_exponent,
            p
        )

        return self.public_value

    def compute_shared_secret(
        self,
        received_public_value,
        p
    ):

        self.shared_secret = modular_exponentiation(
            received_public_value,
            self.private_exponent,
            p
        )

        return self.shared_secret