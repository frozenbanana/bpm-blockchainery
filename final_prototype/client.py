# Client for reading and changing state in BPMN
from Crypto.PublicKey import RSA
from Crypto import Random
import socketserver
import os
import socket
import sys
import ast


class Client(socketserver.BaseRequestHandler):
    # Generate key pairs
    def __init__(self, serverAddress, _id):
        self.id = _id
        self.serverAddress = serverAddress
        self.addresses = []
        self.state = {}

        # Check if keys exsist
        if (os.path.exists('rsa-keys/{}/private.key'.format(self.id))):
            self.read_keypair_from_file()
            self.key = RSA.importKey(self.publickey)
        else:
            self.create_new_keypair()

        print(self.publickey)
        print(self.privatekey)

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())

    def read_keypair_from_file(self):
        print("Reading keys from file")
        with open("rsa-keys/{}/public.key".format(self.id), 'r') as content_file:
            self.publickey = content_file.read()
        with open("rsa-keys/{}/private.key".format(self.id), 'r') as content_file:
            self.privatekey = content_file.read()
        print("Done.")

    def create_new_keypair(self):
        print('Creating new keypair for id: {}'.format(self.id))
        self.key = RSA.generate(2048)
        with open("rsa-keys/{}/private.key".format(self.id), 'w') as content_file:
            os.chmod("rsa-keys/{}/private.key".format(self.id), 0o600)
            content_file.write(self.key.exportKey('PEM').decode())

        with open("rsa-keys/{}/public.key".format(self.id), 'w') as content_file:
            os.chmod("rsa-keys/{}/public.key".format(self.id), 0o600)
            content_file.write(self.key.publickey().exportKey('PEM').decode())

        self.privatekey = self.key.exportKey('PEM').decode()
        self.publickey = self.key.publickey().exportKey('PEM').decode()
        print('Created.')

    def sendMessage(self, message):
        print(self.encrypt(message))

    def encrypt(self, message):
        return self.key.encrypt(message.encode(), 32)

    def decrypt(self, message):
        return self.key.decrypt(message).decode()


# Send encoded message to server
def send(server_address, encoded_message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    sock.sendall(encoded_message)
    recievedMessage = b''
    data = sock.recv(16)
    while data:
        recievedMessage += data
        if data:
            print('received "%s"' % data)
        else:
            break
        data = sock.recv(16)

    sock.close()

    return recievedMessage.decode()


# Program needs 3 argumens
# 1 - client id -> generate unique key pair
# 2 - host        ->
# 3 - port number -> open connect with server
def main():
    server_address = (sys.argv[2], int(sys.argv[3]))
    c = Client(server_address, sys.argv[1])

    # Server Communication

    # Fetch state
    state_package = {'header': 'FETCH_STATE', 'payload': ''}
    message_to_server = str(state_package).encode()
    response = send(server_address, message_to_server)
    c.state = ast.literal_eval(response)
    # print('state is fetched', c.state)

    # Add key
    state_package = {'header': 'ADD_KEY', 'payload': c.publickey}
    message_to_server = str(state_package).encode()
    response = send(server_address, message_to_server)
    c.state = ast.literal_eval(response)
    # print('Key is added', c.state)
    while True:
        print("--------------------------------------")
        print("Welcome to a very private BPMN state machine client. BETA")
        print("What do you want?")
        print("Option 1, check out state")
        print("Option 2, check out addresses")
        print("Option 3, change state")
        print("Option 9, exit")

        option = int(input())
        print("You chose {}".format(option))
        if (option == 1):
            print(c.state['state'])
        elif (option == 2):
            print(c.state['addresses'])
        elif option == 9:
            break

    print("Goodbye")


if __name__ == "__main__":
    main()
    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), Client) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
