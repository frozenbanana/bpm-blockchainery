import uuid
import random
from Crypto.PublicKey import RSA
from Crypto import Random


class client:
    def __init__(self, Chain):
        self.private_key, self.public_key = get_keys()
        self.master = False
        self.sync_key = False
        self.chain = Chain
        self.id = uuid.uuid4()
        self.post_to_chain(self.id, self.public_key)
        self.chain.add_user(self.id, self.public_key)
        self.all_users = {}

    def __repr__(self):
        return "{}".format(self.public_key)

    def make_master(self):
        self.master = True
        self.sync_key = get_sync_key()

    def encrypt_synch(self, msg):
        if not self.sync_key:
            return False
        result = ''
        for letter in str(msg):
            result += str(int(letter) + self.sync_key)
        return int(result)

    def decrypt_synch(self, msg):
        if not self.sync_key:
            return False
        result = ''
        for letter in str(msg):
            result += str(int(letter) - self.sync_key)
        return int(result)

    def post_to_chain(self, key, val):
        self.chain.add_to_storage(key, val)

    def get_from_chain(self, key):
        return self.chain[key]

    def get_all_users(self):
        return self.chain.users

    def post_sync_key(self):
        if self.master:
            self.all_users = self.get_all_users()
            for public_key in self.all_users.values():
                public_key_sync = public_key.encrypt(self.sync_key)
                self.chain.add_to_storage('user-' + public_key, public_key_sync)



def get_sync_key():
    # replace this with something smart
    return 1


def get_keys():
    random_generator = Random.new().read
    new_key = RSA.generate(2048, random_generator)
    public_key = new_key.publickey().exportKey("PEM")
    private_key = new_key.exportKey("PEM")
    return private_key, public_key


"""
TODO
class circle:
    def __init__(self): 
        self.sync_key
"""


# BLOCKCHAIN SIMULATION
class storage_on_chain:
    def __init__(self):
        self.storage = {}
        self.users = {}

    def add_to_storage(self, key, val):
        self.storage[key] = val

    def add_user(self, user, public_key):
        self.users[user] = public_key

    def get_from_storage(self, key):
        if key in self.storage:
            pass

    def pick_master(self):
        ##print('-------------------------------',self.users)
        master_is = random.choice(list(self.users.keys()))
        return master_is



storage = storage_on_chain()
# load clients, if not exist

a = client(storage)
b = client(storage)
c = client(storage)
list_of_clients = [a,b,c]
current_master = storage.pick_master()

for client in list_of_clients:
    if current_master == client.public_key:
        client.make_master() 
msg = 123
encrypted = a.encrypt_synch(msg)
clear = a.decrypt_synch(encrypted)
if clear == msg:
    print('sync encryption works!')
    
    
