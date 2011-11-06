from twisted.internet import reactor, protocol

from stats import Stats
from update import Update
import pickle

import map
import entity
import pygame

class TrotterPub(protocol.Protocol):
    def __init__(self):
        self.first = True

    def dataReceived(self, data):
        up = pickle.loads(data)

        #self.factory.glob.update(up)

        if self.first == True:
            self.first = False
            for layer in self.factory.glob.map.layers:
                for ent in layer.entities:
                    self.transport.write(pickle.dumps(ent.getUpdate(), 2))

            #generate a player
            player = entity.Entity(Stats(0,0),0, "BOB")
            self.factory.glob.update(player)

            self.transport.write(pickle.dumps(player.getUpdate(),2))
        else:
            self.factory.glob.update(up)

            # send to all other clients
            for t in self.factory.transports:
                if t is not self.transport:
                    t.write(pickle.dumps(up,2))

    def connectionMade(self):
        self.factory.transports.append(self.transport)

class MyFactory(protocol.Factory):
    def __init__(self, glob):
        self.clients = []
        self.protocol = TrotterPub
        self.glob = glob
        self.transports = []

    def clientConnectionMade(self, client):
        self.clients.append(client)

    def clientConnectionLost(self, client):
        self.clients.remove(client)


class ServerGlobals:
    def __init__(self):
        self.map = map.generate_map(map.map_width,map.map_height)

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
