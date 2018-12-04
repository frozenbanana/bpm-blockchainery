import random
from Client import client
from Blockchain import storage_on_chain
import ring
import Crypto.PublicKey.RSA
import os

"""
This file will simulate the clients and the blockchain 
"""
"""
storage = storage_on_chain()
# load clients, if not exist

a = client(storage)
b = client(storage)
c = client(storage)
list_of_clients = [a, b, c]
current_master = storage.pick_master()

for client in list_of_clients:
    if current_master == client.public_key:
        client.make_master()
msg = 123
encrypted = a.encrypt_synch(msg)
clear = a.decrypt_synch(encrypted)
if clear == msg:
    print('sync encryption works!')
"""


def _rn(_):
    return Crypto.PublicKey.RSA.generate(1024, os.urandom)


size = 4
message = "Hello"

print "Message is:", message
key = map(_rn, range(size))

r = ring.ring(key)

for i in range(size):
    s1 = r.sign(message, i)
# s2 = r.sign(msg2, i)
    if (i == 1):
        print "Signature is", s1
        print "Signature verified:", r.verify(message, s1)

#    assert r.verify(msg1, s1) and r.verify(msg2, s2) and not r.verify(msg1, s2)
