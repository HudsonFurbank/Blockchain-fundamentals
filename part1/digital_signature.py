# RSA digital signature generation and verification.
# This implements the mathematical RSA operations directly using modular exponentiation.

from record_operations import hash_record


def sign_record(record, sender_name, rsa_keys):
    """
    Signs a record using the sender node's RSA private key.

    Signature formula:
        signature = H(record)^d mod n
    """
    record_string, hash_hex, hash_int = hash_record(record)

    private_d = rsa_keys[sender_name]["d"]
    n = rsa_keys[sender_name]["n"]

    hash_value_for_rsa = hash_int % n
    signature = pow(hash_value_for_rsa, private_d, n)

    return {
        "record_string": record_string,
        "hash_hex": hash_hex,
        "hash_int": hash_int,
        "hash_value_for_rsa": hash_value_for_rsa,
        "signature": signature
    }


def verify_record_signature(record, signature, sender_name, rsa_keys):
    """
    Verifies a sender's RSA signature using the sender's public key.

    Verification formula:
        recovered_hash = signature^e mod n

    The signature is valid when:
        recovered_hash == H(record) mod n
    """
    record_string, hash_hex, hash_int = hash_record(record)

    public_e = rsa_keys[sender_name]["e"]
    n = rsa_keys[sender_name]["n"]

    expected_hash_value = hash_int % n
    recovered_hash_value = pow(signature, public_e, n)

    is_valid = recovered_hash_value == expected_hash_value

    return {
        "record_string": record_string,
        "hash_hex": hash_hex,
        "expected_hash_value": expected_hash_value,
        "recovered_hash_value": recovered_hash_value,
        "is_valid": is_valid
    }