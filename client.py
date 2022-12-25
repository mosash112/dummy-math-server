import socket
import argparse
import os
from tqdm import tqdm


def calculate(sock):
    while(True):
        try:
            op = input("\nEnter desired operation:\n")
            op_in_bytes = str.encode(op)
            sock.sendall(op_in_bytes)
            data = sock.recv(BUFFER_SIZE)
            result = data.decode()
            print("result: "+str(result))
        except KeyboardInterrupt:
            break


def receiveResults(sock, file):
    header = sock.recv(BUFFER_SIZE)
    header_decoded = header.decode()
    header = header_decoded.split("\r\n")
    size = int(header[2].split(" ")[-1])
    progress = tqdm(range(size), f"Receiving {file}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(file, "wb") as f:
        received = 0
        while received < size:
            data = sock.recv(BUFFER_SIZE)
            if data == "":
                break
            received = received + len(data)
            f.write(data)
            progress.update(len(data))


def sendFile(sock, file, size):
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


def handleBatch(sock):
    size = os.path.getsize(batch)
    headers = """\
    POST /auth HTTP/1.1\r
    Content-Type: {content_type}\r
    Content-Length: {content_length}\r
    Host: {host}\r
    Connection: close\r
    \r\n"""

    header_bytes = headers.format(
        content_type="application/txt",
        content_length=size,
        host=str(host) + ":" + str(port)
    ).encode('iso-8859-1')

    sock.sendall(header_bytes)
    sendFile(sock, batch, size)
    receiveResults(s, output)


BUFFER_SIZE = 1024 # send 1024 bytes (1 KB) each time step
LOCALHOST = '127.0.0.1'  # Standard loopback interface address (localhost)

parser = argparse.ArgumentParser(prog = 'client', description = 'a simple dummy "math" client')
parser.add_argument('host', type=str, default=LOCALHOST, help='the IP address of the server host (default:127.0.0.1 which is the localhost)')
parser.add_argument('port', metavar='port',help='the port on which the server is listening')
parser.add_argument('-b', '--batch', type=str, required=False, help='file path of the expressions batch to be sent')
parser.add_argument('-o', '--output', type=str, required=False, help='file path of the json results file')

args = parser.parse_args()
host = args.host
port = int(args.port)
batch = args.batch
output = args.output

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print(f"[+] Connecting to {host}:{port}")
    s.connect((host, port))
    print("[+] Connected.")
    if batch:
        handleBatch(s)
    else:
        calculate(s)
    s.close()