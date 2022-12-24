import socket
import argparse

LOCALHOST = '127.0.0.1'  # Standard loopback interface address (localhost)
parser = argparse.ArgumentParser(
                    prog = 'client',
                    description = 'a simple dummy "math" client')

parser.add_argument('--host', type=str, required=False, default=LOCALHOST, help='the IP address of the server host (default:127.0.0.1 which is the localhost)')
parser.add_argument('port', metavar='port',help='the port on which the server is listening')
parser.add_argument('-b', '--batch', action='store_true', required=False, help='a boolean specify the data sending mode (single expresions or batches)')

args = parser.parse_args()
host = args.host
port = int(args.port)
batch = args.batch


def calculate(sock):
    op = input("\nEnter desired operation:\n")
    op_in_bytes = str.encode(op)
    sock.sendall(op_in_bytes)
    data = sock.recv(1024)
    result = data.decode()
    print("result: "+str(result))


def sendBatch(sock):
    headers = """\
    POST /auth HTTP/1.1\r
    Content-Type: {content_type}\r
    Content-Length: {content_length}\r
    Host: {host}\r
    Connection: close\r
    \r\n"""

    body = 'userName=Mostafa&password=pass'                                 
    body_bytes = body.encode('ascii')
    header_bytes = headers.format(
        content_type="application/json",
        content_length=len(body_bytes),
        host=str(host) + ":" + str(port)
    ).encode('iso-8859-1')

    payload = header_bytes + body_bytes
    payload_in_bytes = str.encode(payload)
    sock.sendall(payload_in_bytes)
    data = sock.recv(1024)
    response = data.decode()
    print("response: "+response)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    print("Connecting to server...\n")
    data = s.recv(1024)
    data = data.decode()
    print(data)
    while(True):
        try:
            if batch:
                sendBatch()
            else:
                calculate(s)
        except KeyboardInterrupt:
            break
