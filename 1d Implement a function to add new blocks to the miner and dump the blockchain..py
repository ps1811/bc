# practical1_blockchain.py

import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
import binascii
import datetime

class Client:
    def __init__(self):
        random = Crypto.Random.new().read
        self._private_key = RSA.generate(1024, random)
        self._public_key = self._private_key.publickey()
        self._signer = PKCS1_v1_5.new(self._private_key)

        self.identity = binascii.hexlify(self._public_key.exportKey(format='DER')).decode('ascii')

class Transaction:
    def __init__(self, sender, recipient, value):
        self.sender = sender
        self.recipient = recipient
        self.value = value
        self.time = datetime.datetime.now()

    def to_dict(self):
        if self.sender == "Genesis":
            identity = "Genesis"
        else:
            identity = self.sender.identity
        return {
            'sender': identity,
            'recipient': self.recipient,
            'value': self.value,
            'time': str(self.time)
        }

    def sign_transaction(self):
        private_key = self.sender._private_key
        signer = PKCS1_v1_5.new(private_key)
        h = SHA.new(str(self.to_dict()).encode('utf8'))
        return binascii.hexlify(signer.sign(h)).decode('ascii')

class Block:
    def __init__(self, previous_hash):
        self.verified_transactions = []
        self.previous_block_hash = previous_hash
        self.nonce = None

def display_transaction(transaction):
    data = transaction.to_dict()
    print("\nSender:", data['sender'])
    print("Recipient:", data['recipient'])
    print("Value:", data['value'])
    print("Time:", data['time'])

if __name__ == "__main__":
    genesis_transaction = Transaction("Genesis", "Network", 500.0)
    block0 = Block(previous_hash=None)
    block0.verified_transactions.append(genesis_transaction)

    blockchain = [block0]

    print("\nBlockchain Dump:")
    for idx, block in enumerate(blockchain):
        print(f"\nBlock #{idx}")
        for tx in block.verified_transactions:
            display_transaction(tx)
n
