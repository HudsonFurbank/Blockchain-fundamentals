from inventoryNode import InventoryNode
from queryHandling import QueryHandler

def createInventoryNodes():
# creates the 4 different invent nodes using the ID's and random values from the supplied list of keys doc. 

    inventoryA = InventoryNode(
        name = "inventory A",
        dataFile = "Part 2 Secure Record Retrieval/data/inventoryA.json",
        identityFile = "Part 2 Secure Record Retrieval/data/inventoryAIdent.json"
    )
    inventoryB = InventoryNode(
        name = "inventory B",
        dataFile = "Part 2 Secure Record Retrieval/data/inventoryB.json",
        identityFile = "Part 2 Secure Record Retrieval/data/inventoryBIdent.json"
    )
    inventoryC = InventoryNode(
        name = "inventory c",
        dataFile = "Part 2 Secure Record Retrieval/data/inventoryC.json",
        identityFile = "Part 2 Secure Record Retrieval/data/inventoryAIdent.json"
    )
    inventoryD = InventoryNode(
        name = "inventory D",
        dataFile = "Part 2 Secure Record Retrieval/data/inventoryD.json",
        identityFile = "Part 2 Secure Record Retrieval/data/inventoryAIdent.json"
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
    if queryResult["accepted"]:
        print("Status: Accepted")
        print(f"Item ID: {queryResult['itemId']}")
        print(f"Quantity: {queryResult['quantity']}")
        print(f"message to sign: {queryResult['canonicalMessage']}")

    else: 
        print("Status: Rejected")

if __name__ == "__main__":
    runQueryDemo()
