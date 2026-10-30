"""
protocol messages and validation
"""

import json
import secrets

from authentication import (
    sign_message,
    verify_signature
)


PROTOCOL = "DH-CLASSROOM-AUTH-v1"

MAX_MESSAGE_SIZE = 4096

def generate_nonce():

    return secrets.token_hex(32)

def encode_message(message):

    return json.dumps(
        message,
        sort_keys=True,
        separators=(",", ":")
    ).encode("utf-8")

def validate_nonce(nonce):

    if not isinstance(nonce, str):
        return False

    if len(nonce) != 64:
        return False

    try:
        int(nonce, 16)
        return True

    except ValueError:
        return False

def create_init_message(
    p,
    g,
    A,
    nonce_A
):

    return {
        "protocol": PROTOCOL,
        "message_type": "init",
        "initiator": "Alice",
        "responder": "Bob",
        "p": p,
        "g": g,
        "A": A,
        "nonce_A": nonce_A
    }

def sign_init_message(
    signing_key,
    message
):

    message_bytes = encode_message(message)

    signature = sign_message(
        signing_key,
        message_bytes
    )

    return signature

def verify_init_message(
    verification_key,
    message,
    signature
):

    message_bytes = encode_message(message)

    return verify_signature(
        verification_key,
        signature,
        message_bytes
    )

def create_transcript(
    p,
    g,
    A,
    B,
    nonce_A,
    nonce_B
):

    return {
        "protocol": PROTOCOL,
        "initiator": "Alice",
        "responder": "Bob",
        "p": p,
        "g": g,
        "A": A,
        "B": B,
        "nonce_A": nonce_A,
        "nonce_B": nonce_B
    }

def create_response_message(transcript):

    return {
        "message_type": "response",
        "transcript": transcript
    }

def sign_response_message(
    signing_key,
    response_message
):

    response_bytes = encode_message(
        response_message
    )

    return sign_message(
        signing_key,
        response_bytes
    )

def verify_response_message(
    verification_key,
    response_message,
    signature
):

    response_bytes = encode_message(
        response_message
    )

    return verify_signature(
        verification_key,
        signature,
        response_bytes
    )

def create_finish_message(transcript):

    return {
        "message_type": "finish",
        "transcript": transcript
    }

def sign_finish_message(
    signing_key,
    finish_message
):

    finish_bytes = encode_message(
        finish_message
    )

    return sign_message(
        signing_key,
        finish_bytes
    )

def verify_finish_message(
    verification_key,
    finish_message,
    signature
):

    finish_bytes = encode_message(
        finish_message
    )

    return verify_signature(
        verification_key,
        signature,
        finish_bytes
    )

def verify_shared_secret(
    alice,
    bob
):

    return (
        alice.shared_secret ==
        bob.shared_secret
    )

if __name__ == "__main__":

    from participant import Participant

    p = 23
    g = 5

    alice = Participant("Alice")
    bob = Participant("Bob")

    alice.private_exponent = 6
    bob.private_exponent = 15

    A = alice.generate_public_value(g, p)
    B = bob.generate_public_value(g, p)

    alice.compute_shared_secret(B, p)
    bob.compute_shared_secret(A, p)

    print(
        verify_shared_secret(
            alice,
            bob
        )
    )