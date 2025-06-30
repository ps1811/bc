# practical2_mining.py

import hashlib

def sha256(message):
    return hashlib.sha256(message.encode('ascii')).hexdigest()

def mine(message, difficulty=1):
    assert difficulty >= 1
    prefix = '1' * difficulty
    for i in range(1000000):
        digest = sha256(str(hash(message)) + str(i))
        if digest.startswith(prefix):
            print(f"After {i} iterations found nonce:\n{digest}")
            return digest
    print("Nonce not found within iteration limit.")
    return None

if __name__ == "__main__":
    mine("welcome", 2)
