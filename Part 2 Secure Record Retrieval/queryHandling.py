from collections import Counter

class QueryHandler:
#   Handles the secure retrieval query workflow before multi-signature.
#   takes query and forwards it to each warehouse inventory node. Checks that each
#   node agrees and then creates a canonical message for hashing and signing  

    def __init__(self, inventoryNodes):
        if not inventoryNodes:
            raise ValueError("At least one inventory node is required")

        self.inventoryNodes = inventoryNodes

    def submitQuery(self, itemId, requestedBy="Procurement Officer"):
        """
        Main query entry point.

        Returns a structured query result object that can later be passed
        into the Harn multi-signature process.
        """
        itemId = str(itemId).strip().zfill(3)

        print("\n================ QUERY SUBMISSION ================")
        print(f"Requested by : {requestedBy}")
        print(f"Item ID      : {itemId}")
        print("Forwarding query to inventory nodes...")

        nodeResults = self.queryAllNodes(itemId)

        print("\n================ NODE SEARCH RESULTS ================")
        for result in nodeResults:
            if result["found"]:
                print(
                    f"{result['node']}: FOUND item {result['itemId']} "
                    f"with quantity {result['quantity']}"
                )
            else:
                print(f"{result['node']}: ITEM NOT FOUND")

        agreementResult = self.checkQuantityAgreement(nodeResults)

        if not agreementResult["accepted"]:
            print("\n================ QUERY RESULT ================")
            print("Query rejected.")
            print(f"Reason: {agreementResult['reason']}")

            return {
                "accepted": False,
                "itemId": itemId,
                "reason": agreementResult["reason"],
                "nodeResults": nodeResults,
                "canonicalMessage": None,
            }

        acceptedQuantity = agreementResult["quantity"]

        approvalResults = self.collectNodeApprovals(itemId, acceptedQuantity)

        print("\n================ NODE APPROVALS ================")
        for approval in approvalResults:
            status = "APPROVED" if approval["approved"] else "REJECTED"
            print(f"{approval['node']}: {status} - {approval['reason']}")

        allApproved = all(approval["approved"] for approval in approvalResults)

        if not allApproved:
            return {
                "accepted": False,
                "itemId": itemId,
                "reason": "Not all nodes approved the proposed result",
                "nodeResults": nodeResults,
                "approvalResults": approvalResults,
                "canonicalMessage": None,
            }

        canonicalMessage = self.buildCanonicalMessage(
            itemId=itemId,
            quantity=acceptedQuantity,
            approvedNodes=[node.name for node in self.inventoryNodes],
        )

        print("\n================ QUERY ACCEPTED ================")
        print(f"Agreed quantity    : {acceptedQuantity}")
        print(f"Approved node count: {len(approvalResults)}/{len(self.inventoryNodes)}")
        print(f"Canonical message  : {canonicalMessage}")

        return {
            "accepted": True,
            "itemId": itemId,
            "quantity": acceptedQuantity,
            "nodeResults": nodeResults,
            "approvalResults": approvalResults,
            "canonicalMessage": canonicalMessage,
        }

    def queryAllNodes(self, itemId):
        """
        Sends the item query to every inventory node.
        """
        results = []

        for node in self.inventoryNodes:
            result = node.searchItem(itemId)
            results.append(result)

        return results

    def checkQuantityAgreement(self, nodeResults):
        """
        Checks whether the nodes agree on the item quantity.

        For a clean assignment demo, strict agreement is easiest:
        - all nodes must find the item
        - all nodes must report the same quantity

        You can later modify this to majority voting if you want.
        """
        foundResults = [result for result in nodeResults if result["found"]]

        if len(foundResults) != len(nodeResults):
            missingNodes = [
                result["node"]
                for result in nodeResults
                if not result["found"]
            ]

            return {
                "accepted": False,
                "reason": f"Item missing from node(s): {', '.join(missingNodes)}",
                "quantity": None,
            }

        quantities = [result["quantity"] for result in foundResults]
        quantityCounts = Counter(quantities)

        if len(quantityCounts) != 1:
            return {
                "accepted": False,
                "reason": f"Inconsistent quantities reported: {dict(quantityCounts)}",
                "quantity": None,
            }

        agreedQuantity = quantities[0]

        return {
            "accepted": True,
            "reason": "All nodes reported the same quantity",
            "quantity": agreedQuantity,
        }

    def collectNodeApprovals(self, itemId, proposedQuantity):
        """
        Asks every node to approve the proposed result.

        In the full Part 2 workflow, only approving nodes should generate
        Harn partial signatures.
        """
        approvals = []

        for node in self.inventoryNodes:
            approval = node.approveQueryResult(itemId, proposedQuantity)
            approvals.append(approval)

        return approvals

    def buildCanonicalMessage(self, itemId, quantity, approvedNodes):
        """
        Creates a stable message format for hashing and signing.

        Important:
        Every node must sign the exact same message.
        Do not use unordered dictionaries directly as the signed message.
        """
        approvedNodesText = ",".join(sorted(approvedNodes))

        message = (
            f"queryType=inventoryQuantity"
            f"|itemId={itemId}"
            f"|quantity={quantity}"
            f"|approvedNodes={approvedNodesText}"
        )

        return message