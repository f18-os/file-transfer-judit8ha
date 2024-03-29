#! /usr/bin/env python3

import socket, sys, re
sys.path.append("../lib")  # for params
import params

from fSock import framedSend, framedReceive

switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--debug'), "debug", False),  # boolean (set if present)
    (('-?', '--usage'), "usage", False),  # boolean (set if present)
)

progname = "framedClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
    params.usage()

try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

s = None
for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        print(" error: %s" % msg)
        s = None
        continue
    try:
        print(" attempting to connect to %s" % repr(sa))
        s.connect(sa)
    except socket.error as msg:
        print(" error: %s" % msg)
        s.close()
        s = None
        continue
    break

if s is None:
    print('could not open socket')
    sys.exit(1)


def put(filename): # FOR FILE SENDING
    try:
        with open(filename) as f:
            payload = f.read()
        framedSend(s, filename.encode('utf-8') + b"/" + payload.encode('utf-8'))
    except FileNotFoundError:
        print("File Not Found")


while True:
    clientIn = input("client:")
    msg = clientIn.split(" ")
    if msg[0] == "put":  #IF PUT THEN MESSAGE GETS SENT AS A FILE
        put(msg[1])
        print("sent file")
    elif msg[0] == "./END":  #THIS WILL CLOSE SOCKET AND END CONNECTION
            sys.exit(1)
    else:
        framedSend(s, clientIn.encode(), debug)
        print("sent msg")
    print("received:", framedReceive(s, debug))
