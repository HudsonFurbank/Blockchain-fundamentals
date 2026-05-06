from inventoryNode import InventoryNode
from queryHandling import QueryHandler
from harnMultiSignature import HarnMultiSignature
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

def createInventoryNodes():
# creates the 4 different invent nodes using the ID's and random values from the supplied list of keys doc. 

    inventoryA = InventoryNode(
        name = "inventory A",
        dataFile = DATA_DIR / "inventoryA.json",
        identityFile = DATA_DIR / "inventoryAIdent.json"
    )
    inventoryB = InventoryNode(
        name = "inventory B",
        dataFile = DATA_DIR / "inventoryB.json",
        identityFile = DATA_DIR / "inventoryBIdent.json"
    )
    inventoryC = InventoryNode(
        name = "inventory c",
        dataFile = DATA_DIR / "inventoryC.json",
        identityFile = DATA_DIR / "inventoryAIdent.json"
    )
    inventoryD = InventoryNode(
        name = "inventory D",
        dataFile = DATA_DIR / "inventoryD.json",
        identityFile = DATA_DIR / "inventoryAIdent.json"
    )

    return [inventoryA, inventoryB, inventoryC, inventoryD]

def runQueryDemo():
    nodes = createInventoryNodes()
    coordinator = QueryHandler(nodes)

    itemId = input("Enter item ID to search:")
    queryResult = coordinator.submitQuery(
        itemId = itemId,
        requestedBy = "Procurement Officer",
    )

    print("\nReturned Object")
    if not queryResult["accepted"]:
        print("Status: Rejected")
        return
    
    print("Status: Accepted")
    print(f"Item ID: {queryResult['itemId']}")
    print(f"Quantity: {queryResult['quantity']}")
    print(f"message to sign: {queryResult['canonicalMessage']}")
    print("Beginning Harn Multi Signature process...")

    harn = HarnMultiSignature(
        pkgFile = DATA_DIR / "PKG.json"
    )

    multiSigResult = harn.signQueryResult(
        canonicalMessage = queryResult["canonicalMessage"],
        inventoryNodes = nodes
    )

    print("\n======== MULTI-SIGNATURE RESULT =========")

    if multiSigResult["valid"]:
        print("Harn multi-signature: VALID")
        print("The query result has been jointly signed by all inventory nodes.")
        print(f"Final signature S = {multiSigResult['groups']}")
    else:
        print("Harn multi-signature: INVALID")
        print("The query result should not be returned to the Procurement Officer.")

if __name__ == "__main__":
    runQueryDemo()
