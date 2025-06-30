# practical1_transactions.py

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
        if self.sender == "LDS":
            identity = "LDS"
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

def display_transaction(transaction):
    data = transaction.to_dict()
    print("\nSender:", data['sender'])
    print("Recipient:", data['recipient'])
    print("Value:", data['value'])
    print("Time:", data['time'])

if __name__ == "__main__":
    clients = [Client() for _ in range(4)]
    transactions = []

    t1 = Transaction(clients[0], clients[1].identity, 15.0)
    t2 = Transaction(clients[0], clients[2].identity, 6.0)
    t3 = Transaction(clients[1], clients[3].identity, 2.0)

    transactions.extend([t1, t2, t3])

    for tx in transactions:
        tx.sign_transaction()
        display_transaction(tx)
