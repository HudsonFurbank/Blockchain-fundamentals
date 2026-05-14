# Simplified PBFT-style quorum consensus for record acceptance.

from digital_signature import verify_record_signature


FAULTY_NODES_TOLERATED = 1


def node_vote(node_name, sender_name, record, signature, rsa_keys):
    """
    Each node verifies the sender's digital signature.
    If verification succeeds, the node votes ACCEPT.
    Otherwise, it votes REJECT.
    """
    verification_result = verify_record_signature(
        record=record,
        signature=signature,
        sender_name=sender_name,
        rsa_keys=rsa_keys
    )

    vote = "ACCEPT" if verification_result["is_valid"] else "REJECT"

    print(f"\n{node_name} verification")
    print(f"Record string        : {verification_result['record_string']}")
    print(f"SHA-256 hash         : {verification_result['hash_hex']}")
    print(f"Expected hash mod n  : {verification_result['expected_hash_value']}")
    print(f"Recovered sig^e mod n: {verification_result['recovered_hash_value']}")
    print(f"Signature valid?     : {verification_result['is_valid']}")
    print(f"{node_name} vote       : {vote}")

    return vote


def run_consensus(sender_name, record, signature, inventory_nodes, rsa_keys):
    """

    For four nodes and f = 1 faulty node:
        required approvals = 2f + 1 = 3

    The record is accepted only when at least three nodes vote ACCEPT.
    """
    total_nodes = len(inventory_nodes)
    required_approvals = (2 * FAULTY_NODES_TOLERATED) + 1

    print("\n================ CONSENSUS STAGE ================")
    print(f"Consensus type       : Simplified PBFT-style quorum")
    print(f"Total nodes          : {total_nodes}")
    print(f"Fault tolerance f    : {FAULTY_NODES_TOLERATED}")
    print(f"Required approvals   : {required_approvals} out of {total_nodes}")

    votes = {}

    for node_name in inventory_nodes:
        votes[node_name] = node_vote(
            node_name=node_name,
            sender_name=sender_name,
            record=record,
            signature=signature,
            rsa_keys=rsa_keys
        )

    accept_count = list(votes.values()).count("ACCEPT")
    reject_count = list(votes.values()).count("REJECT")
    accepted = accept_count >= required_approvals

    global_decision = "COMMIT / ACCEPT RECORD" if accepted else "ABORT / REJECT RECORD"

    print("\n================ CONSENSUS RESULT ================")
    print(f"Votes        : {votes}")
    print(f"Accept count : {accept_count}")
    print(f"Reject count : {reject_count}")
    print(f"Final decision for all nodes: {global_decision}")

    return {
        "accepted": accepted,
        "votes": votes,
        "accept_count": accept_count,
        "reject_count": reject_count,
        "required_approvals": required_approvals,
        "global_decision": global_decision
    }