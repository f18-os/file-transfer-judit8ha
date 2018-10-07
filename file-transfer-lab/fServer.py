#! /usr/bin/env python3

import sys, os, socket, re
sys.path.append("../lib")       # for params
import params

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
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
            if payload:
                for p in payload:
                    if p == b'~':
                        f = payload[:b'~']
                        payload = payload[b'~':]
                        break

                if len(f) > 1:
                    if debug: print("-File Received-")
                    file= open(f, 'w')
                    file.write(payload)
                    file.close()
                    payload += b'got file!'

                if debug: print("rec'd: ", payload)
                if not payload:
                    if debug: print("child exiting")
                    sys.exit(0)
                framedSend(sock, payload, debug)
            else:
                if debug: print("no payload received")
