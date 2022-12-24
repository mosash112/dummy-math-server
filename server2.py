import socket
import argparse
import os
from evaluate import function_creator

LOCALHOST = '127.0.0.1'  # Standard loopback interface address (localhost)
parser = argparse.ArgumentParser(
                    prog = 'server2',
                    description = 'a simple dummy "math" server')

parser.add_argument('--host', type=str, required=False, default=LOCALHOST, help='the IP address of the server host (default:127.0.0.1 which is the localhost)')
parser.add_argument('port', metavar='port',help='the port which the server uses as a listening socket')

args = parser.parse_args()
host = args.host
port = int(args.port)


def handlingConnection(conn, addr):
    with conn:
        print(f"Connected by {addr}")
        conn.sendall(b'accepted connection.')
        while True:
            data = conn.recv(1024)
            if not data:
                break
            data_decoded = data.decode()
            result = function_creator(data_decoded)
            result = str.encode(str(result))
            conn.sendall(result)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen()
    s.setblocking(False)
    while(True):
        try:
            conn, addr = s.accept()
            ret = os.fork()
            if ret == 0:
                handlingConnection(conn, addr)
            break
        except KeyboardInterrupt:
            break
    s.close()
