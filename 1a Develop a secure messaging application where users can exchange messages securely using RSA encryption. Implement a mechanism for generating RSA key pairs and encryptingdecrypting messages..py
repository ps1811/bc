# practical1_secure_messaging.py

#pip install pycryptodome
import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
import binascii

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

    def to_dict(self):
        if self.sender == "Genesis":
            identity = "Genesis"
        else:
            identity = self.sender.identity
        return {
            'sender': identity,
            'recipient': self.recipient,
            'value': self.value
        }

    def sign_transaction(self):
        private_key = self.sender._private_key
        signer = PKCS1_v1_5.new(private_key)
        h = SHA.new(str(self.to_dict()).encode('utf8'))
        return binascii.hexlify(signer.sign(h)).decode('ascii')

if __name__ == "__main__":
    client1 = Client()
    client2 = Client()

    print("Client 1 identity:", client1.identity)
    print("Client 2 identity:", client2.identity)

    transaction = Transaction(client1, client2.identity, 10.0)
    signature = transaction.sign_transaction()
    print("Transaction signature:", signature)
