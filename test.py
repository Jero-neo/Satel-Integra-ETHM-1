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


def makeCRC16():
    nr1 = "14"
    nr2 = "7A"

    out1 = binToHex(leftRotate(hexToBin(nr1)))
    out2 = binToHex(leftRotate(hexToBin(nr2)))
    a = int(out1[2] + out1[3] + out2[2] + out2[3], 16)
    b = 0xffff
    return hex(a ^ b)


def makeCRC32(crc16):
    # print(crc16)
    var1 = crc16[2] + crc16[3]
    var2 = crc16[4] + crc16[5]
    hout1 = binToHex(leftRotate(hexToBin(var1)))
    hout2 = binToHex(leftRotate(hexToBin(var2)))
    a = int(hout1[2] + hout1[3] + hout2[2] + hout2[3], 16)
    b = 0xffff
    return hex(a ^ b)
        


def makeCMD(cmd, cmd2=''):
    retour = makeCRC16() 
    CRChigh = retour[2] + retour[3]
    CRClow = retour[4] + retour[5]
    retour = int(retour, 0)
    somhigh = int('0x' + CRChigh, 0)
    somcmd = int('0x' + cmd, 0)
    som = retour + somhigh + somcmd
    som_hex = hex(som)
    if cmd2:
        retour2 = makeCRC32(som_hex)
        CRChigh2 = retour2[2] + retour2[3]
        retour2 = int(retour2, 0)
        somhigh2 = int('0x' + CRChigh2, 0)
        somcmd2 = int('0x' + cmd2, 0)
        som2 = retour2 + somhigh2 + somcmd2
        som_hex2 = hex(som2)

        CRChigh2 = som_hex2[2] + som_hex2[3]
        CRClow2 = som_hex2[4] + som_hex2[5]

        s1 = bytearray(unhexlify('FE'))
        s2 = bytearray(unhexlify('FE'))

        d1 = bytearray(unhexlify(cmd)) # cmd
        d2 = bytearray(unhexlify(cmd2)) # cmd2
        d3 = bytearray(unhexlify(CRChigh2)) # CRChigh
        d4 = bytearray(unhexlify(CRClow2)) # CRClow

        e1 = bytearray(unhexlify('FE'))
        e2 = bytearray(unhexlify('0D'))
        cmd = s1+s2+d1+d2+d3+d4+e1+e2
        return cmd
    else:
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


print(connect(makeCMD('00', 'ff'))) # zone 32BIT
print(connect(makeCMD('00', '17'))) # zone 32BIT
print(connect(makeCMD('17', 'ff'))) # zone 32BIT
print(connect(makeCMD('7c'))) # INT-RS/ETHM-1 module version
print(connect(makeCMD('7e'))) # INTEGRA version
