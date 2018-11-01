import random
from Client import client
from Blockchain import storage_on_chain

"""
This file will simulate the clients and the blockchain 
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
