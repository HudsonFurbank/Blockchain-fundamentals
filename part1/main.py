#demonstration file 

from rsa_operations import initialise_all_rsa_keys, print_rsa_key_summary
from storage_manager import (
    load_all_inventory_nodes,
    store_record_in_all_nodes,
    display_all_node_records
)
from digital_signature import sign_record
from consensus_protocol import run_consensus
from new_record_data import SENDER_NODE, NEW_RECORD


def print_section(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def demonstrate_valid_record_insertion(rsa_keys, inventory_nodes):
    """
    Demonstrates the normal Part 1 workflow:
    1. Inventory A creates a new record.
    2. Inventory A signs the record.
    3. All nodes verify the signature.
    4. Nodes run consensus.
    5. Accepted record is stored in all local inventories.
    """
    print_section("PART 1 DEMO: VALID RECORD INSERTION")

    sender = SENDER_NODE
    new_record = NEW_RECORD.copy()

    print("\n================ RECORD CREATION ================")
    print(f"Originating node: {sender}")
    print(f"New record      : {new_record}")

    signing_result = sign_record(
        record=new_record,
        sender_name=sender,
        rsa_keys=rsa_keys
    )

    signature = signing_result["signature"]

    print("\n================ DIGITAL SIGNATURE GENERATION ================")
    print(f"Formatted record        : {signing_result['record_string']}")
    print(f"SHA-256 hash            : {signing_result['hash_hex']}")
    print(f"Hash value used for RSA : {signing_result['hash_value_for_rsa']}")
    print(f"Generated signature     : {signature}")

    consensus_result = run_consensus(
        sender_name=sender,
        record=new_record,
        signature=signature,
        inventory_nodes=inventory_nodes,
        rsa_keys=rsa_keys
    )

    if consensus_result["accepted"]:
        store_record_in_all_nodes(new_record, inventory_nodes)
        print("\nStorage result: Record accepted and stored in every inventory node.")
    else:
        print("\nStorage result: Record rejected and not stored.")

    display_all_node_records(inventory_nodes)


def demonstrate_tampered_record_rejection(rsa_keys, inventory_nodes):
    """
    Demonstrates integrity protection:
    The sender signs the original record, but the record is changed before verification.
    The verification should fail because the hash no longer matches the signature.
    """
    print_section("OPTIONAL DEMO: TAMPERED RECORD REJECTION")

    sender = SENDER_NODE
    original_record = NEW_RECORD.copy()

    signing_result = sign_record(
        record=original_record,
        sender_name=sender,
        rsa_keys=rsa_keys
    )

    signature = signing_result["signature"]

    tampered_record = original_record.copy()
    tampered_record["quantity"] = 99

    print("\nOriginal signed record :", original_record)
    print("Tampered record        :", tampered_record)
    print("Original signature     :", signature)

    consensus_result = run_consensus(
        sender_name=sender,
        record=tampered_record,
        signature=signature,
        inventory_nodes=inventory_nodes,
        rsa_keys=rsa_keys
    )

    if consensus_result["accepted"]:
        store_record_in_all_nodes(tampered_record, inventory_nodes)
        print("\nStorage result: Tampered record was accepted.")
    else:
        print("\nStorage result: Tampered record rejected and not stored.")

    display_all_node_records(inventory_nodes)


def main():
    rsa_keys = initialise_all_rsa_keys()
    inventory_nodes = load_all_inventory_nodes()

    while True:
        print("\n\n================ SECURE DLT INVENTORY SYSTEM ================")
        print("1. Show RSA parameters")
        print("2. Show current inventory records")
        print("3. Run valid record insertion demo")
        print("4. Run tampered record rejection demo")
        print("0. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            print_rsa_key_summary(rsa_keys)
        elif choice == "2":
            display_all_node_records(inventory_nodes)
        elif choice == "3":
            demonstrate_valid_record_insertion(rsa_keys, inventory_nodes)
        elif choice == "4":
            demonstrate_tampered_record_rejection(rsa_keys, inventory_nodes)
        elif choice == "0":
            print("Exiting demonstration.")
            break
        else:
            print("Invalid choice. Please select 0, 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()