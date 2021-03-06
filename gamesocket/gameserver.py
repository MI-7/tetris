import socketserver, gamesocket
from logger import *

rooms = {}
userop = {}
games = {}
shapes = {}


class GameClientHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP gamesocket connected to the client
        self.data = self.request.recv(1024).strip()
        tlog(MDEBUG, "{} wrote:".format(self.client_address[0]))
        tlog(MDEBUG, self.data)

        data = self.data.decode().split()
        command = data[0]

        if command == 'register':
            tlog(MDEBUG, "data=", data, "; ", "command=", command)
            uname = data[1]
            userop[uname] = None
            self.request.sendall(b'0 success')
        elif command == 'createroom':
            tlog(MDEBUG, "data=", data, "; ", "command=", command)
            roomname = data[1]
            uname = data[2]

            if roomname in rooms.keys():
                tlog(MDEBUG, "room already exists: " + roomname)
                self.request.sendall(b'1 room already exists')
                return
            rooms[roomname] = [uname]
            games[roomname] = 0
            userop[uname] = {}
            tlog(MDEBUG, rooms)
            self.request.sendall(b'0 success')
        elif command == 'joinroom':
            tlog(MDEBUG, "data=", data, "; ", "command=", command)
            roomname = data[1]
            uname = data[2]

            if roomname not in rooms.keys():
                tlog(MDEBUG, "room does not exist: " + roomname)
                self.request.sendall(b'2 room does not exist')
                return

            rooms[roomname].append(uname)
            userop[uname] = {}
            tlog(MDEBUG, rooms)
            self.request.sendall(b'0 success')
        elif command == "listroom":
            tlog(MDEBUG, "data=", data, "; ", "command=", command)
            if len(rooms.keys()) >= 1:
                resp = ' '.join(['0'] + list(rooms.keys()))
                self.request.sendall(bytes(resp, "utf-8"))
            else:
                self.request.sendall(b'3 no rooms available')
        elif command == 'queryopponent':
            tlog(MDEBUG, "data=", data, "; ", "command=", command)
            roomname = data[1]

            if roomname not in rooms.keys():
                tlog(MDEBUG, "room does not exist: " + roomname)
                self.request.sendall(b'2 room does not exist')
                return

            tlog(MDEBUG, rooms)
            response = ''
            if len(rooms[roomname]) == 2:
                response = rooms[roomname][1]

            self.request.sendall(bytes(response, 'utf-8'))
        elif command == 'querymainuser':
            tlog(MDEBUG, "data=", data, "; ", "command=", command)
            roomname = data[1]

            if roomname not in rooms.keys():
                tlog(MDEBUG, "room does not exist: " + roomname)
                self.request.sendall(b'2 room does not exist')
                return

            tlog(MDEBUG, rooms)
            response = ''
            if len(rooms[roomname]) > 0:
                response = rooms[roomname][0]

            self.request.sendall(bytes(response, 'utf-8'))
        elif command == 'gamestart':
            tlog(MDEBUG, "data=", data, "; ", "command=", command)
            roomname = data[1]

            if roomname not in rooms.keys():
                tlog(MDEBUG, "room does not exist: " + roomname)
                self.request.sendall(b'2 room does not exist')
                return

            games[roomname] = 1
            self.request.sendall(b'0 success')
        elif command == 'querygamestart':
            tlog(MDEBUG, "data=", data, "; ", "command=", command)
            roomname = data[1]

            if roomname not in rooms.keys():
                tlog(MDEBUG, "room does not exist: " + roomname)
                self.request.sendall(b'2 room does not exist')
                return

            response = str(games[roomname])
            self.request.sendall(bytes(response, 'utf-8'))
        elif command == 'submitshapes':
            tlog(MDEBUG, "data=", data, "; ", "command=", command)
            uname = data[1]
            shape = data[2]

            shapes[uname] = shape
            self.request.sendall(b'0 success')
        elif command == 'getshapes':
            tlog(MDEBUG, "data=", data, "; ", "command=", command)
            uname = data[1]

            response = bytes(shapes[uname], 'utf-8')
            shapes[uname] = ''
            self.request.sendall(response)
        elif command == 'submitkeyseq':
            print(MDEBUG, "data=", data, "; ", "command=", command, 'userop=', userop)
            uname = data[1]
            oppo = data[2]
            myshapeid = data[3]
            opshapeid = data[4]
            keyseq = ''

            if len(data) == 6:
                keyseq = data[5]

            if myshapeid in userop[uname].keys():
                userop[uname][myshapeid] = userop[uname][myshapeid] + keyseq
            else:
                userop[uname][myshapeid] = keyseq

            response = ''
            if opshapeid in userop[oppo].keys():
                response = userop[oppo][opshapeid]

                if len(response) >= 5:
                    userop[oppo][opshapeid] = response[5:]
                    response = response[0:5]
                else:
                    userop[oppo][opshapeid] = ''

            self.request.sendall(bytes(response, 'utf-8'))

        # just send back the same data, but upper-cased
        # self.request.sendall(self.data.upper())

