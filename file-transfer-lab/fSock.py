import re


def framedSend(sock, payload, debug=1):
    if debug: print("framedSend: sending %d byte message" % len(payload))
    msg = str(len(payload)).encode() + b':' + payload
    while len(msg):
        nsent = sock.send(msg)
        msg = msg[nsent:]


rbuf = b""  # static receive buffer


def framedReceive(sock, debug=1):
    if debug: print("receiving")
    global rbuf
    state = "getLength"
    msgLength = -1
    while True:
        if (state == "getLength"):
            if debug: print("getLength State")
            match = re.match(b'([^:]+):(.*)', rbuf, re.DOTALL | re.MULTILINE)  # look for colon
            if match:
                lengthStr, rbuf = match.groups()
                try:
                    msgLength = int(lengthStr)
                    if debug: print("receiving msg size:", msgLength)
                except:
                    if len(rbuf):
                        print("badly formed message length:", lengthStr)
                        return None
                state = "getPayload"
        if state == "getPayload":
            if debug: print("get Payload")
            if len(rbuf) >= msgLength:
                payload = rbuf[0:msgLength]
                rbuf = rbuf[msgLength:]
                return payload
        r = sock.recv(100)
        rbuf += r
        if len(r) == 0:
            if len(rbuf) != 0:
                print("FramedReceive: incomplete message. \n  state=%s, length=%d, rbuf=%s" % (state, msgLength, rbuf))
            return None
        if debug: print("FramedReceive: state=%s, length=%d, rbuf=%s" % (state, msgLength, rbuf))
