from math import gcd
from rsa_keys import RAW_RSA_KEYS


def derive_rsa_parameters(p, q, e):
    """
    Derives RSA modulus n, Euler's totient phi(n), and private exponent d.
    """
    n = p * q
    phi = (p - 1) * (q - 1)

    if gcd(e, phi) != 1:
        raise ValueError("Invalid RSA public exponent. e must be coprime with phi(n).")

    d = pow(e, -1, phi)
    return n, phi, d

def initialise_all_rsa_keys():
    """
    Creates a complete RSA key dictionary for all inventory nodes.
    The original p, q and e are hardcoded in rsa_keys.py.
    This function derives n, phi and d for each node.
    """
    complete_keys = {}

    for node_name, values in RAW_RSA_KEYS.items():
        p = values["p"]
        q = values["q"]
        e = values["e"]

        n, phi, d = derive_rsa_parameters(p, q, e)

        complete_keys[node_name] = {
            "p": p,
            "q": q,
            "e": e,
            "n": n,
            "phi": phi,
            "d": d
        }

    return complete_keys

def print_rsa_key_summary(rsa_keys):
    """
    Prints the RSA parameters used during the demonstration.
    """
    print("\n RSA PARAMETER INITIALISATION")

    for node_name, values in rsa_keys.items():
        print(f"\n{node_name}")
        print(f"p   = {values['p']}")
        print(f"q   = {values['q']}")
        print(f"e   = {values['e']}")
        print(f"n   = {values['n']}")
        print(f"phi = {values['phi']}")
        print(f"d   = {values['d']}")