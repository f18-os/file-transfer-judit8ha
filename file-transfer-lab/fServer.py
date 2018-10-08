#! /usr/bin/env python3

import sys, os, socket, re
sys.path.append("../lib")       # for params
import params

switchesVarDefaults = (
    (('-l', '--listenPort'), 'listenPort', 50001),
    (('-d', '--debug'), "debug", True),  # boolean (set if present)
    (('-?', '--usage'), "usage", False),  # boolean (set if present)
    )

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)

content = b""
while True:
    sock, addr = lsock.accept()
    f = ""

    from fSock import framedSend, framedReceive

    if not os.fork():
        print("new child process handling connection from", addr)
        while True:
            if debug: print("entered loop")
            payload = framedReceive(sock, debug)
            if debug: print("received payload")
            match = re.match(b"([^/]+)/(.*)", content, re.DOTALL | re.MULTILINE)  # look for colon
            if match:
                f, content = match.groups()
                if len(f) > 1:
                    if debug: print("-File Received-")
                    file = open(f, 'w')
                    file.write(content + "modified")
                    file.close()
                    content += b'got file!'
                    if debug: print("rec'd: ", content)
                    framedSend(sock, content, debug)
                else:
                    if debug: print("-message received-")
                    print(content)
                    framedSend(sock, content, debug)
            else:
                if debug: print("no payload received")
                if debug: print("child exiting")
                break
            sys.exit(0)
    sys.exit(0)