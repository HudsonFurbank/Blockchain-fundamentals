import json
from pathlib import Path


class SecureDelivery:

    def __init__(self, procurementFile):
        self.procurementFile = Path(procurementFile)

        with open(self.procurementFile, "r", encoding="utf-8") as file:
            procurementData = json.load(file)

        self.p = int(procurementData["p"])
        self.q = int(procurementData["q"])
        self.e = int(procurementData["e"])

        self.n = self.p * self.q
        self.phi = (self.p - 1) * (self.q - 1)

        # Procurement Officer private exponent
        self.d = pow(self.e, -1, self.phi)

        # RSA can only encrypt integers smaller than n.
        # This gives a safe byte block size.
        self.blockSize = (self.n.bit_length() - 1) // 8

    def encryptText(self, plaintext):
        """
        Encrypts text using the Procurement Officer's RSA public key.

        Encryption:
            c = m^e mod n
        """

        plaintextBytes = plaintext.encode("utf-8")

        cipherBlocks = []
        blockLengths = []

        for i in range(0, len(plaintextBytes), self.blockSize):
            block = plaintextBytes[i:i + self.blockSize]

            blockLengths.append(len(block))

            messageInt = int.from_bytes(block, byteorder="big")
            cipherInt = pow(messageInt, self.e, self.n)

            cipherBlocks.append(str(cipherInt))

        return {
            "cipherBlocks": cipherBlocks,
            "blockLengths": blockLengths
        }

    def decryptText(self, encryptedPackage):
        """
        Decrypts text using the Procurement Officer's RSA private key.

        Decryption:
            m = c^d mod n
        """

        cipherBlocks = encryptedPackage["cipherBlocks"]
        blockLengths = encryptedPackage["blockLengths"]

        recoveredBytes = b""

        for cipherText, blockLength in zip(cipherBlocks, blockLengths):
            cipherInt = int(cipherText)

            messageInt = pow(cipherInt, self.d, self.n)

            blockBytes = messageInt.to_bytes(blockLength, byteorder="big")

            recoveredBytes += blockBytes

        return recoveredBytes.decode("utf-8")