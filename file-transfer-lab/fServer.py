#! /usr/bin/env python3

import sys, os, socket, re,
sys.path.append("../lib")       # for params
import params

switchesVarDefaults = (
    (('-l', '--listenPort'), 'listenPort', 50001),
    (('-d', '--debug'), "debug", False),  # boolean (set if present)
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
    msgType = "" #MESSAGE RECEIVED TYPE - FILE OR MESSAGE -

    from fSock import framedSend, framedReceive

    if not os.fork():
        print("new child process handling connection from", addr)
        while True:
            payload = framedReceive(sock, debug)
            if debug: print("rec'd: ", payload)
            try:
                p = payload.decode().split('/')
                if sys.path(p[0]+'RC'):
                    print("FILE ALREADY EXISTS. OVERWRITE?")
                f = open(p[0]+'RC', 'w')
                f.write(p[1])
                f.close()
                msgType = b"FILE"
                print("-file saved-")
            except:
                msgType = b"MESSAGE"

            if not payload:
                if debug: print("CONNECTION TO CLIENT ENDED")
                sys.exit(1)  #END CONNECTION WITH NO ERROR MESSAGES
            payload = b"received: " + msgType
            framedSend(sock, payload, debug)