import hashlib

#converts the hash of a string into an integer
def hashToInt(message):
    messageBytes = message.encode("utf-8")
    hashHex = hashlib.sha256(messageBytes).hexdigest()
    return int(hashHex, 16)


