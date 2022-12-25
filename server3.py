import socket
import argparse
import random
import os
from tqdm import tqdm
import json
from evaluate import function_creator


def receiveFile(conn, file):
    header = conn.recv(BUFFER_SIZE)
    header_decoded = header.decode()
    header = header_decoded.split("\r\n")
    size = int(header[2].split(" ")[-1])
    progress = tqdm(range(size), f"Receiving {file}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(file, "wb") as f:
        received = 0
        while received < size:
            data = conn.recv(BUFFER_SIZE)
            if data == "":
                break
            received = received + len(data)
            f.write(data)
            progress.update(len(data))


def jsonResults(file, jfile):
    with open(file, "r") as f:
        index = 1
        query = []
        for line in f:
            expr = line.replace("\n", "")
            res = function_creator(expr)
            query.append({"id":index,"requestedLine":expr,"result":str(res)})
            index = index + 1
        dict = {
            "qid":random.randrange(0,9999),
            "query":query
        }
        with open(jfile, "w") as j:
            json.dump(dict,j)


def sendFile(sock, file):
    size = os.path.getsize(file)
    headers = """\
    POST /auth HTTP/1.1\r
    Content-Type: {content_type}\r
    Content-Length: {content_length}\r
    Host: {host}\r
    Connection: close\r
    \r\n"""

    header_bytes = headers.format(
        content_type="application/json",
        content_length=size,
        host=str(host) + ":" + str(port)
    ).encode('iso-8859-1')
    sock.sendall(header_bytes)

    progress = tqdm(range(size), f"Sending {file}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(file, "rb") as f:
        sent = 0
        while sent < size:
            bytes_read = f.read(BUFFER_SIZE)
            if bytes_read == "":
                break
            msg = sock.send(bytes_read)
            sent = sent + msg
            progress.update(msg)


def handlingConnection(conn):
    with conn:
        file = "server3/expressions.txt"
        jfile = "server3/server.json"
        receiveFile(conn, file)
        jsonResults(file, jfile)
        sendFile(conn, jfile)
    conn.close()


BUFFER_SIZE = 1024 # send 1024 bytes (1 KB) each time step
LOCALHOST = '127.0.0.1'  # Standard loopback interface address (localhost)
parser = argparse.ArgumentParser(prog = 'server3', description = 'a simple dummy "math" server')
parser.add_argument('--host', type=str, required=False, default=LOCALHOST, help='the IP address of the server host (default:127.0.0.1 which is the localhost)')
parser.add_argument('port', metavar='port',help='the port which the server uses as a listening socket')

args = parser.parse_args()
host = args.host
port = int(args.port)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen()
    while(True):
        try:
            print(f"[*] Listening as {host}:{port}")
            conn, addr = s.accept()
            print(f"\n[+] {addr} is connected.")
            ret = os.fork()
            if ret == 0:
                handlingConnection(conn)
                break
        except KeyboardInterrupt:
            break
    s.close()
