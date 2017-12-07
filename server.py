import socketserver
from logger import *
from gamesocket.gameserver import GameClientHandler
from globals import *

if __name__ == '__main__':
    HOST, PORT = SERVER_HOST, SERVER_PORT

    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), GameClientHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        tlog(MDEBUG, "server started")
        server.serve_forever()
        tlog(MDEBUG, "entered handler loop")