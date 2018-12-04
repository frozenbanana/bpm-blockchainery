import uuid
from Crypto import Random
from Crypto.PublicKey import RSA

class client:
    """
    simulate a client
    """
    def __init__(self, name): #, Chain):
        self.name = name
        self.private_key, self.public_key = client.get_keys()
        self.sync_key = False
        # self.chain = Chain
        self.id = uuid.uuid4()
        # self.post_to_chain(self.id, self.public_key)
        # self.chain.add_user(self.id, self.public_key)
        # self.all_users = {}
    
    @staticmethod
    def get_sync_key():
        # replace this with something smart
        return 1

    @staticmethod
    def get_keys():
        random_generator = Random.new().read
        new_key = RSA.generate(2048, random_generator)
        public_key = new_key.publickey().exportKey("PEM")
        private_key = new_key.exportKey("PEM")
        return private_key, public_key
    

    def __repr__(self):
        return "This is The client {} with the public key {}".format(self.name, self.public_key)


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
        raise NotImplementedError
        self.chain.add_to_storage(key, val)

    def get_from_chain(self, key):
        raise NotImplementedError
        return self.chain[key]

    def get_all_users(self):
        raise NotImplementedError
        return self.chain.users

    def post_sync_key(self):
        raise NotImplementedError
        if self.master:
            self.all_users = self.get_all_users()
            for public_key in self.all_users.values():
                public_key_sync = public_key.encrypt(self.sync_key)
                self.chain.add_to_storage('user-' + public_key, public_key_sync)
