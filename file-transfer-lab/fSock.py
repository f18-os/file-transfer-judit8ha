import re, os, sys


def redirect_read(filename, fd):  #FD0 read from file not keyboard <
    os.close(fd)  # redirect child's stdin
    sys.stdin = open(filename, "r")
    f = sys.stdin.fileno()
    os.set_inheritable(f, True)


def redirect_write(filename, sock):  #FD1 write to a file not to screen >
    os.close(fdd)  # redirect child's stdout
    sys.stdout = open(filename, "w")
    f = sys.stdout.fileno()  # os.open("p4-output.txt", os.O_CREAT)
    os.set_inheritable(f, True)


def put(sock, filename):
    try:
        payload = filename.read()
        msg = str(len(open(filename).read())).encode() + b':' + filename.encode() + b':' + payload.encode()
        #bts = 0
        while len(msg):
            nsent = sock.send(msg[:100])
            #bts += 100
            msg = msg[nsent:]
    except FileNotFoundError:
        print("File Not Found")


def framedSend(sock, payload, debug=0):
     if debug: print("framedSend: sending %d byte message" % len(payload))
     msg = str(len(payload)).encode() + b':' + payload.encode()
     while len(msg):
         nsent = sock.send(msg)
         msg = msg[nsent:]


rbuf = b""                      # static receive buffer

def framedReceive(sock, debug=0):
    global rbuf
    state = "getLength"
    msgLength = -1
    fileName = None
    while True:
         if (state == "getLength"):
             match = re.match(b'([^:]+):([^:]+):(.*)', rbuf)  # look for colon
             if match:
                  lengthStr, fn, rbuf = match.groups()
                  if rbuf is None:
                      rbuf = fn

                  try:
                       msgLength = int(lengthStr)
                  except:
                       if len(rbuf):
                            print("badly formed message length:", lengthStr)
                            return None
                  state = "getPayload"
         if state == "getPayload":
             if fn:
                 doc = open(fn, "w")
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
