from Crypto import Random

class storage_on_chain:
    """
    simulate blockchain
    """
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
        # print('-------------------------------',self.users)
        master_is = random.choice(list(self.users.keys()))
        return master_is


"""
TODO
class circle:
    def __init__(self): 
        self.sync_key
"""
