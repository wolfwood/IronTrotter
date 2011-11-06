from twisted.internet import reactor, protocol

from stats import Stats
from update import Update
import pickle

import map
import pygame

class TrotterPub(protocol.Protocol):
    def dataReceived(self, data):
        up = pickle.loads(data)

        self.factory.glob.update(up)

        # send to all other clients
        for layer in self.factory.glob.map.layers:
            for ent in layer.entities:
                self.transport.write(pickle.dumps(ent.getUpdate(), 2))

class MyFactory(protocol.Factory):
    def __init__(self, glob):
        self.clients = []
        self.protocol = TrotterPub
        self.glob = glob

    def clientConnectionMade(self, client):
        self.clients.append(client)

    def clientConnectionLost(self, client):
        self.clients.remove(client)


class ServerGlobals:
    def __init__(self):
        self.map = map.generate_map(10,10)

    def update(self, up):
        if up.name != "":
            self.map.addPlayer(up)

def main():
    """This runs the protocol on port 8000"""

    pygame.init()

    screen = pygame.display.set_mode((1,1))

    glob = ServerGlobals()

    factory = MyFactory(glob)

    reactor.listenTCP(8000,factory)
    reactor.run()

# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()
