""" 
Contains the square-and-multiply implementation
"""


def modular_exponentiation(base, exponent, modulus):
    """
    Computes (base^exponent) mod modulus using
    square-and-multiply.
    Returns int
    """

    # Validate inputs
    if not isinstance(base, int):
        raise TypeError("Base must be an integer.")

    if not isinstance(exponent, int):
        raise TypeError("Exponent must be an integer.")

    if not isinstance(modulus, int):
        raise TypeError("Modulus must be an integer.")

    if exponent < 0:
        raise ValueError("Exponent must not be a negative.")

    if modulus <= 0:
        raise ValueError("Modulus must be positive.")

    result = 1 % modulus
    base = base % modulus

    while exponent > 0:

        if exponent % 2 == 1:
            result = (result * base) % modulus

        base = (base * base) % modulus
        exponent //= 2

    return result