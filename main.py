from parameters import (
    generate_prime,
    validate_modulus,
    find_generator
)

from participant import Participant

from authentication import (
    generate_signing_keys
)

from protocol import (
    generate_nonce,
    create_init_message,
    sign_init_message,
    verify_init_message,
    create_transcript,
    create_response_message,
    sign_response_message,
    verify_response_message,
    create_finish_message,
    sign_finish_message,
    verify_finish_message
)

bits = 16

p, generation_time = generate_prime(bits)

print(f"Requested prime size: {bits} bits")
print("Modulus generated using library prime generator")

print(
    "Received modulus library validation:",
    "PASS" if validate_modulus(p) else "FAIL"
)

g = find_generator(p)

print("Generator: validated")

alice = Participant("Alice")
bob = Participant("Bob")
alice.generate_private_exponent(p)
bob.generate_private_exponent(p)
A = alice.generate_public_value(g, p)
B = bob.generate_public_value(g, p)

alice_private_key, alice_public_key = (
    generate_signing_keys()
)

bob_private_key, bob_public_key = (
    generate_signing_keys()
)

nonce_A = generate_nonce()

init_message = create_init_message(
    p,
    g,
    A,
    nonce_A
)

init_signature = sign_init_message(
    alice_private_key,
    init_message
)

if verify_init_message(
    alice_public_key,
    init_message,
    init_signature
):
    print("Alice initiation signature: VALID")

nonce_B = generate_nonce()

transcript = create_transcript(
    p,
    g,
    A,
    B,
    nonce_A,
    nonce_B
)

response_message = create_response_message(
    transcript
)

response_signature = sign_response_message(
    bob_private_key,
    response_message
)

if verify_response_message(
    bob_public_key,
    response_message,
    response_signature
):
    print("Bob response signature: VALID")

finish_message = create_finish_message(
    transcript
)

finish_signature = sign_finish_message(
    alice_private_key,
    finish_message
)

if verify_finish_message(
    alice_public_key,
    finish_message,
    finish_signature
):
    print("Alice finish signature: VALID")

alice.compute_shared_secret(B, p)
bob.compute_shared_secret(A, p)

if alice.shared_secret == bob.shared_secret:

    print("\nTranscript authenticated: YES")
    print(
        "Shared-secret equality in local test: PASS"
    )

else:

    print(
        "Shared-secret equality in local test: FAIL"
    )