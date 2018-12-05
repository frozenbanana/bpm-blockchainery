import random
from Client import client
# from Blockchain import storage_on_chain
import ring_signature
import Crypto.PublicKey.RSA
import os
import argparse
import socket
import time


def callback_print(message):
    print('received message: {}'.format(message))


def main(args, possible_roles):
    """
    start a client with arguments specified by user
    client will connect to localhost:(1234 + client_name_index)
    """

    try:
        cli = client(args.role)
    except Exception as e:
        print('client creation failed with exception {}. Arguments were {}'.format(e.message, args))

    cli.make_receiver()

    cli.make_receive_message(callback_print, 3)

    if cli.name == 'buyer':
        cli.send_to('seller', 'hi from buyer')
    else:
        cli.send_to('buyer', 'hi from seller')
    
    while True: 
        time.sleep(1)

    print("created the client {}".format(cli.name))

    size = args.num_clients
    print("expecting a total number of {} clients participating in the ring signature".format(
        size))
    message = "Hello"

    print("Message is:", message)
    key = map(ring_signature.ring.rn, range(size))

    r = ring_signature.ring(key)

    for i in range(size):
        s1 = r.sign(message, i)
        if (i == 1):
            print("Signature is", s1)
            print("Signature verified:", r.verify(message, s1))

    #    assert r.verify(msg1, s1) and r.verify(msg2, s2) and not r.verify(msg1, s2)
    


if __name__ == "__main__":
    """
    main function. initiate argument parser
    """
    possible_roles = ['buyer', 'seller']

    parser = argparse.ArgumentParser(
        description='Start client with specified role')
    parser.add_argument('--role',
                        choices=possible_roles,
                        help='this is the role of the client. Possible roles are {}'.format(
                            ', '.join(possible_roles)),
                        required=True)

    """
    parser.add_argument('--num_clients', type=int,
                        help='the total number of clients involved in the communication',
                        required=True)
    """

    main(parser.parse_args(), possible_roles)
