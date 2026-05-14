import hashlib


def format_record(record):
    """
    Converts a record into a fixed string format.

    Every node must use the same format before hashing.
    Otherwise, the same record could produce different hashes.
    """
    return f"{record['item_id']}|{record['quantity']}|{record['price']}|{record['location']}"


def hash_record(record):
    """
    Hashes a formatted record using SHA-256.

    The hash is returned in three forms:
    1. formatted record string
    2. hexadecimal hash
    3. integer hash for RSA modular arithmetic
    """
    record_string = format_record(record)
    hash_hex = hashlib.sha256(record_string.encode("utf-8")).hexdigest()
    hash_int = int(hash_hex, 16)

    return record_string, hash_hex, hash_int


def records_are_same(record_one, record_two):
    """
    Compares two records using their fixed formatted representation.
    """
    return format_record(record_one) == format_record(record_two)