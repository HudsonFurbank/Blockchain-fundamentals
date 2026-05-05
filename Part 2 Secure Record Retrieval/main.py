from inventoryNode import InventoryNode
from queryHandling import QueryHandler

def createInventoryNodes():
# creates the 4 different invent nodes using the ID's and random values from the supplied list of keys doc. 

    inventoryA = InventoryNode(
        name = "inventory A",
        identityId = 126,
        randomValue = 621,
        dataFile = "Part 2 Secure Record Retrieval/data/inventoryA.json",
    )
    inventoryB = InventoryNode(
        name = "inventory B",
        identityId = 127,
        randomValue = 721,
        dataFile = "Part 2 Secure Record Retrieval/data/inventoryB.json",
    )
    inventoryC = InventoryNode(
        name = "inventory c",
        identityId = 128,
        randomValue = 821,
        dataFile = "Part 2 Secure Record Retrieval/data/inventoryC.json",
    )
    inventoryD = InventoryNode(
        name = "inventory D",
        identityId = 129,
        randomValue = 921,
        dataFile = "Part 2 Secure Record Retrieval/data/inventoryD.json",
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
