__author__ = 'Tim Schughart'

import socket
import argparse
import base64
import signal
import threading


def signal_handler(signal, frame):
    print("Ctrl + C recognized, exiting")
    s.close()
    exit(0)

def commander(command, s): #TODO Multithreading of command execution
    pass

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--target", action="store", dest="target", help="Specifies target ip address", nargs=1, type=str)
parser.add_argument("-p", "--port", action="store", dest="port", help="Specifies destination port", nargs=1, type=int)

args = parser.parse_args()

try :
    port = args.port[0]
except Exception as e:
    print("Could not parse port argument, see help with -h")
    print(e)
    exit(1)

try :
    target = args.target[0]
except Exception as e:
    print("Could not parse target argument, see help with -h")
    print(e)
    exit(1)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.connect((target, port))
except Exception as e:
    print("Could not connect to target - maby firewall blocking our request?")
    exit(1)

while True:
    command = base64.b64encode(input('> ').encode('ASCII'))
    s.send(command)
    response = base64.b64decode(s.recv(1024))
    print(response)
#    t1 = threading.Thread(target=commander, args=(command, s)) TODO Implemnting function of command mutli Threading
#    t1.start
