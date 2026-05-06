import json
from pathlib import Path


class InventoryNode:
#   Represents one inventory node in the distributed inventory system.

    def __init__(self, name, dataFile, identityFile):
        self.name = name
        self.dataFile = Path(dataFile)
        self.identityFile = Path(identityFile)

        self.records = self.loadRecords()

        self.identityData = self.loadIdentityData()
        self.identityId = int(self.identityData["identityId"])
        self.randomValue = int(self.identityData["randomValue"])

    def loadRecords(self):
#   Loads the records from the inventory's .json

        with open(self.dataFile, "r", encoding="utf-8") as file:
            records = json.load(file)

        return records
    
    def loadIdentityData(self):

        with open(self.identityFile, "r", encoding="utf-8") as file:
            identityData = json.load(file)
        
        return identityData

    def searchItem(self, itemId):
#   Searches this node's local records for the requested item.
        itemId = str(itemId).strip().zfill(3)

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

    def approveQueryResult(self, itemId, acceptedQuantity):
        """
        Checks whether this node agrees with the accepted quantity.

        This is useful before multi-signature generation.
        A node should only sign if its local data matches the accepted result.
        """
        localResult = self.searchItem(itemId)

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
    
    def savePrivateKey(self, privateKey):
        with open(self.identityFile, "r", encoding = "utf-8") as file:
            identityData = json.load(file)

        identityData["privateKey"] = str(privateKey)

        with open(self.identityFile, "w", encoding = "utf-8") as file:
            json.dump(identityData, file, indent = 4)

        self.savePrivateKey = int(privateKey)
