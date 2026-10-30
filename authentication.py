"""
for Ed25519 signing and verification
"""

from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey
)

from cryptography.exceptions import InvalidSignature

def generate_signing_keys():

    signing_key = Ed25519PrivateKey.generate()

    verification_key = signing_key.public_key()

    return signing_key, verification_key

def sign_message(signing_key, message_bytes):

    return signing_key.sign(message_bytes)

def verify_signature(
    verification_key,
    signature,
    message_bytes
):

    try:

        verification_key.verify(
            signature,
            message_bytes
        )

        return True

    except InvalidSignature:

        return False
