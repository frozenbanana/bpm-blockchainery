import uuid
import os
import time
import threading
from Crypto import Random
from Crypto.PublicKey import RSA


class client:
    """
    simulate a client
    """

    def __init__(self, name):  # , Chain):
        self.name = name
        self.private_key, self.public_key = client.get_keys()
        self.sync_key = False
        # self.chain = Chain
        self.id = uuid.uuid4()
        # self.post_to_chain(self.id, self.public_key)
        # self.chain.add_user(self.id, self.public_key)
        # self.all_users = {}
        self.inbox = None

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

    def make_receiver(self):
        """
        make client be able to receive messages
        """
        if not self.inbox:
            self.inbox = os.path.join(os.path.dirname(
                os.path.abspath(__file__)), self.name + '.txt')
        #with open(self.inbox, 'w') as f:
         #   pass

    def make_receive_message(self, callback, frequency):
        """
        create a handler for a received message
        @param callback: the function to call on receive message
        @param frequency: check interval in seconds
        """
        def receive_message():
            while True:
                msg = ''
                try:
                    with open(self.inbox, 'r') as f:
                        msg = f.read()
                except:
                    pass
                if msg != '':
                    # clear inbox
                    callback(msg)
                    with open(self.inbox, 'w') as f:
                        pass
                    msg == ''
                time.sleep(frequency)
        thread = threading.Thread(target=receive_message, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()
        print('registered callback function on receive message')

    def send_to(self, receiver, message):
        """
        send to a other client
        @param receiver: the other client
        @param message: the message send to the receiver
        """
        success = False
        while not success:
            try:
                with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), receiver + '.txt'), 'w') as f:
                    f.write(message)
                success = True
            except:
                time.sleep(5)

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
        #self.chain.add_to_storage(key, val)

    def get_from_chain(self, key):
        raise NotImplementedError
        # return self.chain[key]

    def get_all_users(self):
        raise NotImplementedError
        # return self.chain.users

    def post_sync_key(self):
        raise NotImplementedError
        """
        if self.master:
            self.all_users = self.get_all_users()
            for public_key in self.all_users.values():
                public_key_sync = public_key.encrypt(self.sync_key)
                self.chain.add_to_storage(
                    'user-' + public_key, public_key_sync)
        """
