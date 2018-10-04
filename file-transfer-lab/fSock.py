import re, os, sys

def put(sock, filename,debug=1):
    try:
        with open(filename) as f: payload = f.read()
        #payload = "".join(payload)
        msg = str(len(payload)).encode() + b':' + filename.encode() + b':' + payload.encode()
        if debug: print("framedSend: sending %d byte file" % len(payload))
        while len(msg):
            nsent = sock.send(msg[:100])
            msg = msg[nsent:]
    except FileNotFoundError:
        print("File Not Found")


def framedSend(sock, payload, debug=1):
    if debug: print("framedSend: sending %d byte message" % len(payload))
    msg = str(len(payload)).encode() + b':' + payload.encode()
    while len(msg):
        nsent = sock.send(msg[:100])
        msg = msg[nsent:]


rbuf = b""                      # static receive buffer
#fileName = None
#file = None

def framedReceive(sock, debug=1):
    global rbuf
    fileName = None
    file = None
    state = "getLength"
    msgLength = -1
    while True:
        if (state == "getLength"):
            if debug: print("getLength State")
            match = re.match(b'([^:]+):([^:]+):(.*)', rbuf, re.DOTALL | re.MULTILINE)  # look for colon
            if match:
                if debug: print("matched file")
                lengthStr, fn, rbuf = match.groups()
                if rbuf is None:
                    if debug: print("message")
                    rbuf = fn
                else:
                    if debug: print("file")
                    fileName = fn
                try:
                    msgLength = int(lengthStr)
                except:
                    if len(rbuf):
                        print("badly formed message length:", lengthStr)
                        return None
                state = "getPayload"
        if state == "getPayload":
            if fileName:
                file = open(fileName, "wb")
                #if len(rbuf) >= msgLength:
                #    payload = rbuf[0:msgLength]
                #    rbuf = rbuf[msgLength:]
                #    return payload
        r = sock.recv(100)
        print("r  ", r)
        rbuf += r
        print(rbuf)
        if debug: print("FramedReceive: state=%s, length=%d, rbuf=%s" % (state, msgLength, rbuf))
        if len(r) == 0:
            if len(rbuf) != 0:
                print("FramedReceive: incomplete message. \n  state=%s, length=%d, rbuf=%s" % (state, msgLength, rbuf))
                return None
            if file: file.write(rbuf)
            #return None
        if debug: print("FramedReceive: state=%s, length=%d, rbuf=%s" % (state, msgLength, rbuf))
    return None
