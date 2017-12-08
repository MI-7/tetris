import socket
import traceback
from logger import *
import sys
from globals import *


def createsocket(host, port):
    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        tlog(MDEBUG, "socket opened")
    except Exception as err:
        s = None
        tlog(MDEBUG, "sock creation failed")
        tlog(MERROR, err)
        traceback.print_exc()

    return s


def closesocket(s):
    try:
        s.close()
        tlog(MDEBUG, "socket closed")
    except Exception as err:
        s = None
        tlog(MERROR, err)
        traceback.print_exc()


def sendcommand(s, cmd):
    response = None
    try:
        s.send(bytes(cmd, "utf-8"))
        response = s.recv(1024)
        if type(response) is bytes:
            response = response.decode()
    except Exception as err:
        response = None
        tlog(MERROR, err)
        traceback.print_exc()

    tlog(MDEBUG, "cmd=", cmd, "; response=", response)

    return response


def login(uname):
    s = createsocket(SERVER_HOST, SERVER_PORT)
    if s is None:
        sys.exit(-1)

    response = sendcommand(s, ''.join(['register', ' ', uname]))

    s.close()

    return int(response.split()[0])


def createroom(roomname, uname):
    s = createsocket(SERVER_HOST, SERVER_PORT)
    if s is None:
        sys.exit(-1)

    response = sendcommand(s, ''.join(['createroom', ' ', roomname, ' ', uname]))

    s.close()

    return int(response.split()[0])


def joinroom(roomname, uname):
    s = createsocket(SERVER_HOST, SERVER_PORT)
    if s is None:
        sys.exit(-1)

    response = sendcommand(s, ''.join(['joinroom', ' ', roomname, ' ', uname]))

    s.close()

    return int(response.split()[0])


def listroom():
    s = createsocket(SERVER_HOST, SERVER_PORT)
    if s is None:
        sys.exit(-1)

    response = sendcommand(s, ''.join(['listroom']))

    s.close()
    rooms = response.split()

    if rooms[0] != '0':
        # not successful, return empty list
        return []
    else:
        return rooms[1:]


def queryopponent(roomname):
    s = createsocket(SERVER_HOST, SERVER_PORT)
    if s is None:
        sys.exit(-1)

    response = sendcommand(s, ''.join(['queryopponent', ' ', roomname]))

    s.close()

    return response


def querymainuser(roomname):
    s = createsocket(SERVER_HOST, SERVER_PORT)
    if s is None:
        sys.exit(-1)

    response = sendcommand(s, ''.join(['querymainuser', ' ', roomname]))

    s.close()

    return response


def gamestart(roomname):
    s = createsocket(SERVER_HOST, SERVER_PORT)
    if s is None:
        sys.exit(-1)

    response = sendcommand(s, ''.join(['gamestart', ' ', roomname]))

    s.close()

    return int(response.split()[0])


def querygamestart(roomname):
    s = createsocket(SERVER_HOST, SERVER_PORT)
    if s is None:
        sys.exit(-1)

    response = sendcommand(s, ''.join(['querygamestart', ' ', roomname]))

    s.close()

    return int(response.split()[0])


def submitshapes(uname, shapes):
    s = createsocket(SERVER_HOST, SERVER_PORT)
    if s is None:
        sys.exit(-1)

    response = sendcommand(s, ''.join(['submitshapes', ' ', uname, ' ', shapes]))

    s.close()

    return int(response.split()[0])


def getshapes(uname):
    s = createsocket(SERVER_HOST, SERVER_PORT)
    if s is None:
        sys.exit(-1)

    response = sendcommand(s, ''.join(['getshapes', ' ', uname]))

    s.close()

    return response


def submitkeyseq(uname, oppo, keyseq):
    s = createsocket(SERVER_HOST, SERVER_PORT)
    if s is None:
        sys.exit(-1)

    response = sendcommand(s, ''.join(['submitkeyseq', ' ', uname, ' ', oppo, ' ', keyseq]))

    s.close()

    return response


if __name__ == "__main__":
    login('leon')
    print(listroom())
    print(joinroom('SNAP', 'jane'))
    createroom('SNAP', 'leon')
    createroom('SNAP', 'leon')
    print(joinroom('SNAP', 'jane'))
    print(joinroom('SNAP2', 'john'))
    createroom('SNAP2', 'leon2')
    print(listroom())
    print(queryopponent('SNAP'))
    print(queryopponent('SNAP2'))
    print(querymainuser('SNAP'))
    print(gamestart('SNAP'))
    print(querygamestart('SNAP'))
    print(submitshapes('leon', '0123495858'))
    print(getshapes('leon'))
    print(getshapes('leon'))
    print(submitkeyseq('leon', 'jane', '01230123'))
    print(submitkeyseq('jane', 'leon', '32103210'))
    print(submitkeyseq('leon', 'jane', '01010101'))