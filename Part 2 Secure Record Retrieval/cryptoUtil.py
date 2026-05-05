import hashlib

def extendedGcd(a, b):
    if b == 0:
        return a, 1, 0
    
    gcd, x1, y1 = extendedGcd(b, a % b)

    x = y1
    y = x1 - (a // b) * y1

    return gcd, x, y

def modInverse(a, m):
    gcd, x, y = extendedGcd(a, m)

    if gcd != 1:
        raise ValueError("modular inverse does not exist")
    
    return x % m

def multiplyMod(values, mod):
    result = 1

    for value in values:
        result = (result * value) % mod
    
    return result

#converts the hash of a string into an integer
def hashToInt(message):
    messageBytes = message.encode("utf-8")
    hashHex = hashlib.sha256(messageBytes).hexdigest()
    return int(hashHex, 16)


