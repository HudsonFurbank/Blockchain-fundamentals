# Inventory node local storage operations.

from inventory_a_data import INVENTORY_A_RECORDS
from inventory_b_data import INVENTORY_B_RECORDS
from inventory_c_data import INVENTORY_C_RECORDS
from inventory_d_data import INVENTORY_D_RECORDS
from record_operations import records_are_same


def copy_records(records):
    """
    Creates a safe copy of a node's local records.
    """
    return [record.copy() for record in records]


def load_all_inventory_nodes():
    """
    Loads each inventory node's local data from its own separate file.
    """
    return {
        "Inventory A": copy_records(INVENTORY_A_RECORDS),
        "Inventory B": copy_records(INVENTORY_B_RECORDS),
        "Inventory C": copy_records(INVENTORY_C_RECORDS),
        "Inventory D": copy_records(INVENTORY_D_RECORDS)
    }


def store_record_in_all_nodes(record, inventory_nodes):
    """
    Stores an accepted record in every inventory node's local storage.

    A duplicate check is included so the same demonstration is not stored twice
    in the same run.
    """
    for node_name, records in inventory_nodes.items():
        already_exists = any(records_are_same(existing, record) for existing in records)

        if not already_exists:
            records.append(record.copy())


def display_all_node_records(inventory_nodes):
    """
    Displays every inventory node's local records.
    """
    print("\n================ LOCAL INVENTORY STORAGE ================")

    for node_name, records in inventory_nodes.items():
        print(f"\n{node_name}")
        print("-" * len(node_name))

        for record in records:
            print(
                f"Item ID: {record['item_id']} | "
                f"Quantity: {record['quantity']} | "
                f"Price: {record['price']} | "
                f"Location: {record['location']}"
            )