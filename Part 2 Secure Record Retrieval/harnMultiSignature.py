from cryptoUtil import hashToInt
import json

class HarnMultiSignature:

    def __init__(self, pkgFile):
        
        with open(pkgFile, "r", encoding = "utf-8") as file:
            pkgData = json.load(file)
        
        self.p = int(pkgData["p"])
        self.q = int(pkgData["q"])
        self.e = int(pkgData["e"])

        self.n = self.p * self.q
        self.phi = (self.p - 1) * (self.q - 1)

        #d = e^-1 mod phi(n)
        self.d = pow(self.e, -1, self.phi)

        self.pkgFile = pkgFile

    def signQueryResult(self, canonicalMessage, inventoryNodes):
        print("\n===========Harn Multi-Sign===========")

        print("\nLoaded PKG values from:")
        print(f"{self.pkgFile}")
        
        print("\nPKG values:")
        print(f"p = {self.p}")
        print(f"q = {self.q}")
        print(f"e = {self.e}")
        print(f"n = {self.n}")
        print(f"d = {self.d}")

        g_i = {}
        t_i = {}
        s_i = {}

        print("\nStep 1: Calculate each inventorys private identity key: g_i")
        
        for node in inventoryNodes:
            g = pow(node.identityId, self.d, self.n)
            g_i[node.name] = g
            node.savePrivateKey(g)

            print(f"{node.name}:")
            print(f"ID = {node.identityId}")
            print(f"g_{node.name} = node ID^d mod n")
            print(f"g_{node.name} = {g}")

        print("\nStep 2: Generate each inventories t_i value:")

        groupt = 1

        for node in inventoryNodes:
            t = pow(node.randomValue, self.e, self.n)
            t_i[node.name] = t
            groupt = (groupt * t) % self.n

            print(f"{node.name}:")
            print(f"r_{node.name} = {node.randomValue}")
            print(f"t_{node.name} = node rand value^e mod n")
            print(f"t_{node.name} = {t}")
        
        print("\nStep 3: group t calculation")
        print("t = (t_inventoryA * t_inventoryB * t_inventoryC * t_inventoryD) mod n")
        print(f"t = {groupt}")

        hashInput = f"{groupt},{canonicalMessage}"
        messageHash = hashToInt(hashInput)

        print("\nStep 4: Message to Hash:")
        print("h = H(t, message)")
        print(f"message = {canonicalMessage}")
        print(f"h = {messageHash}")

        groupS = 1

        for node in inventoryNodes:
            g = g_i[node.name]

            s = g * pow(node.randomValue, messageHash, self.n) % self.n

            s_i[node.name] = s
            groupS = (groupS * s) % self.n

            print(f"{node.name}:")
            print("s = g * r^Hash(t, m) mod n")
            print(f"s = {s}")

        print("\nStep 6: Combine s_i for final signature")
        print(" S = (s_inventoryA * s_inventoryB * s_inventoryC * s_inventoryD) mod n")
        print(f"S = {groupS}")
        
        identityProduct = 1

        for node in inventoryNodes:
            identityProduct = (identityProduct * node.identityId) % self.n

        left = pow(groupS, self.e, self.n)

        right = (
            identityProduct * pow(groupt, messageHash, self.n)
        ) % self.n

        valid = left == right

        print("\nStep 7: Verify S")
        print("Check S^e mod n == product(id_i) * t^h mod n")
        print(f"left = {left}")
        print(f"right = {right}")
        print(f"Valid = {valid}")

        print("\nStep 8: concensus check")
        consensusVotes = {}

        for node in inventoryNodes:
            consensusVotes[node.name] = valid
            print(f"{node.name}: {'ACCEPT' if valid else 'REJECT'}")
        
        consensusAccepted = all(consensusVotes.values())
        print(f"Concensus accepted = {consensusAccepted}")

        return {
            "canonicalMessage": canonicalMessage,
            "groupt": groupt,
            "messageHash": messageHash,
            "s_i": s_i,
            "groups" : groupS,
            "signerIds": [node.identityId for node in inventoryNodes],
            "valid": valid,
            "consensusVotes": consensusVotes,
            "consensusAccepted": consensusAccepted,
        }
    
    def verifySignaturePackage(self, canonicalMessage, groupt, aggregateSignature, signerIds):
# Procurement Officer verifies the Harn multi-signature after decrypting the received response.
# Uses the same verification equation: S^e mod n == product(ID_i) * t^h mod n

        hashInput = f"{groupt},{canonicalMessage}"
        messageHash = hashToInt(hashInput)

        identityProduct = 1

        for identityId in signerIds:
            identityProduct = (identityProduct * int(identityId)) % self.n

        left = pow(int(aggregateSignature), self.e, self.n)

        right = (
            identityProduct * pow(int(groupt), messageHash, self.n)
        ) % self.n

        valid = left == right

        return {
            "valid": valid,
            "messageHash": messageHash,
            "left": left,
            "right": right
    }
