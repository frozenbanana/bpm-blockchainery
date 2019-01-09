import socketserver
import sys
import json
import ast


class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def operation(self, option):
        # print("Inside operation ", type(option))
        # print("Inside operation ", option)
        if option['header'] == 'FETCH_STATE':
            response = self.state
        elif option['header'] == 'ADD_KEY': 
            self.state['addresses'].append(option['payload'])
            response = self.state
        else:
            response = "Invalid option." 
        
        return response


    def handle(self):
        with open('state.json') as data:
            self.state = json.load(data)
            data.close()

        
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        # Convert to dict
        req = self.data.decode('ascii')
        req = ast.literal_eval(req)
        print(req)
        # Find out correct response
        response = self.operation(req)
        print('Response: ')
        print(response)
        # Send it to client
        self.request.sendall(str(response).encode())

        with open('state.json', 'w+') as data:
            # Formatting
            response = str(response)
            response = response.replace("\'", "\"")
            response = response.replace("False", "false")
            # Write new state
            data.write(response)
            data.close()
    
if __name__ == "__main__":

    HOST, PORT = sys.argv[1], int(sys.argv[2])

    # Create the server, binding to localhost on port 9999
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
