#!/usr/bin/python

#
#   Example Satel Integra ETHM-1 module TCP/IP connection
#

import socket
from binascii import unhexlify


def connect(cmd):

    # testopstelling
    host = "10.0.1.248"
    port = 7094

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(cmd)
        data = s.recv(1024)

    return data


def hexToBin(hex):
    res = "{0:08b}".format(int(hex, 16))
    return str(res)


def leftRotate(st):
    n0 = st[0]
    n1 = st[1]
    n2 = st[2]
    n3 = st[3]
    n4 = st[4]
    n5 = st[5]
    n6 = st[6]
    n7 = st[7]
    return n1+n2+n3+n4+n5+n6+n7+n0


def binToHex(bin):
    return hex(int(bin, 2))


def makeCRC():
    nr1 = "14"
    nr2 = "7A"

    out1 = binToHex(leftRotate(hexToBin(nr1)))
    out2 = binToHex(leftRotate(hexToBin(nr2)))
    a = int(out1[2] + out1[3] + out2[2] + out2[3], 16)
    b = 0xffff
    return hex(a ^ b)


def makeCMD(cmd):
    retour = makeCRC() 
    CRChigh = retour[2] + retour[3]
    CRClow = retour[4] + retour[5]
    retour = int(retour, 0)
    somhigh = int('0x' + CRChigh, 0)
    somcmd = int('0x' + cmd, 0)
    som = retour + somhigh + somcmd
    som_hex = hex(som)
    CRChigh = som_hex[2] + som_hex[3]
    CRClow = som_hex[4] + som_hex[5]

    s1 = bytearray(unhexlify('FE'))
    s2 = bytearray(unhexlify('FE'))

    d1 = bytearray(unhexlify(cmd)) # cmd
    d2 = bytearray(unhexlify(CRChigh)) # CRChigh
    d3 = bytearray(unhexlify(CRClow)) # CRClow

    e1 = bytearray(unhexlify('FE'))
    e2 = bytearray(unhexlify('0D'))
    cmd = s1+s2+d1+d2+d3+e1+e2
    return cmd


print(connect(makeCMD('7c'))) # INT-RS/ETHM-1 module version
print(connect(makeCMD('7e'))) # INTEGRA version
