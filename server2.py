import socket
import argparse
import os
import logging
from evaluate import function_creator


def handlingConnection(conn, addr):
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            data_decoded = data.decode()
            logging.info(f"receiving expresion from client on port {addr[1]}")
            logging.info("exprission: "+data_decoded)
            result = function_creator(data_decoded)
            logging.info("result: "+str(result))
            result = str.encode(str(result))
            conn.sendall(result)


LOCALHOST = '127.0.0.1'  # Standard loopback interface address (localhost)
parser = argparse.ArgumentParser(prog = 'server2', description = 'a simple dummy "math" server')
parser.add_argument('--host', type=str, required=False, default=LOCALHOST, help='the IP address of the server host (default:127.0.0.1 which is the localhost)')
parser.add_argument('port', metavar='port',help='the port which the server uses as a listening socket')

args = parser.parse_args()
host = args.host
port = int(args.port)

logging.basicConfig(filename='server2.log', filemode='a', encoding='utf-8', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen()
    while(True):
        try:
            logging.info(f"[*] Listening as {host}:{port}")
            conn, addr = s.accept()
            logging.info(f"[+] {addr} is connected.")
            ret = os.fork()
            if ret == 0:
                handlingConnection(conn, addr)
                break
        except KeyboardInterrupt as k:
            logging.error("server terminated")
            break
    s.close()
