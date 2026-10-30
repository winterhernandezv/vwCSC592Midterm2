"""
for prime generation and parameter validation.
"""

import secrets
import time

from Crypto.Util.number import getPrime
from Crypto.Util.number import isPrime
from modular_math import modular_exponentiation

def generate_prime(bits=16):

    if isinstance(bits, bool):
        raise TypeError("Bit length must be an integer.")

    if not isinstance(bits, int):
        raise TypeError("Bit length must be an integer.")

    if bits < 16 or bits > 32:
        raise ValueError("Prime size must be between 16 and 32 bits.")

    start_time = time.perf_counter()

    p = getPrime(bits, randfunc=secrets.token_bytes)

    end_time = time.perf_counter()

    if p.bit_length() != bits:
        raise ValueError("Generated prime has incorrect bit length.")

    if p % 2 == 0:
        raise ValueError("Generated prime is not odd.")

    generation_time = end_time - start_time

    return p, generation_time


def validate_modulus(p):

    if isinstance(p, bool):
        return False

    if not isinstance(p, int):
        return False

    if p.bit_length() < 16 or p.bit_length() > 32:
        return False

    if not isPrime(p):
        return False

    return True

def prime_factors(n):

    if not isinstance(n, int):
        raise TypeError("n must be an integer.")

    if n < 1:
        raise ValueError("n must be positive.")

    factors = set()

    # Remove all factors of 2
    while n % 2 == 0:
        factors.add(2)
        n //= 2

    divisor = 3

    # Check odd divisors
    while divisor * divisor <= n:

        while n % divisor == 0:
            factors.add(divisor)
            n //= divisor

        divisor += 2

    # Remaining prime factor
    if n > 1:
        factors.add(n)

    return factors

def is_generator(g, p, factors):

    for r in factors:

        result = modular_exponentiation(
            g,
            (p - 1) // r,
            p
        )

        if result == 1:
            return False

    return True

def find_generator(p):

    factors = prime_factors(p - 1)

    for g in range(2, p - 1):

        if is_generator(g, p, factors):
            return g

    raise ValueError("No generator found.")
