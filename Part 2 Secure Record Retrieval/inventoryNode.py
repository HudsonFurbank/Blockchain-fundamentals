import json
from pathlib import Path


class InventoryNode:
#   Represents one inventory node in the distributed inventory system.

    def __init__(self, name, identityId, randomValue, dataFile):
        self.name = name
        self.identityId = identityId
        self.randomValue = randomValue
        self.dataFile = Path(dataFile)
        self.records = self.load_records()

    def load_records(self):
#   Loads the records from the inventory's .json

        with open(self.dataFile, "r", encoding="utf-8") as file:
            records = json.load(file)

        return records

    def search_item(self, itemId):
        """
        Searches this node's local records for the requested item.

        Returns a dictionary with:
        - found: True/False
        - node: node name
        - itemId
        - quantity
        - full record
        """

        for record in self.records:
            if str(record.get("itemId")).zfill(3) == itemId:
                return {
                    "node": self.name,
                    "found": True,
                    "itemId": itemId,
                    "quantity": int(record["quantity"]),
                    "record": record,
                }

        return {
            "node": self.name,
            "found": False,
            "itemId": itemId,
            "quantity": None,
            "record": None,
        }

    def approve_query_result(self, itemId, acceptedQuantity):
        """
        Checks whether this node agrees with the accepted quantity.

        This is useful before multi-signature generation.
        A node should only sign if its local data matches the accepted result.
        """
        localResult = self.search_item(itemId)

        if not localResult["found"]:
            return {
                "node": self.name,
                "approved": False,
                "reason": "Item not found locally",
            }

        if localResult["quantity"] != acceptedQuantity:
            return {
                "node": self.name,
                "approved": False,
                "reason": (
                    f"Local quantity {localResult['quantity']} does not match "
                    f"proposed quantity {acceptedQuantity}"
                ),
            }

        return {
            "node": self.name,
            "approved": True,
            "reason": "Local record matches proposed query result",
        }