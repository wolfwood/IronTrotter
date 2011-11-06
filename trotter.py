from twisted.internet import reactor, protocol

import sys

from stats import Stats
import pickle

from twisted.internet.task import LoopingCall

import pygame
import colors
import map


class TrotterSub(protocol.Protocol):
    """Once connected, send a message, then print the result."""

    def connectionMade(self):
        self.transport.write("hello, world!")

    def dataReceived(self, data):
        "As soon as any data is received, write it back."
        s = pickle.loads(data)
        print "Server said:", s.x, s.y, s.hp

    def connectionLost(self, reason):
        print "connection lost"


# this connects the protocol to a server runing on port 8000
def main():
    addr = "localhost"
    if len(sys.argv) > 1:
        addr = sys.argv[1]

    pygame.init()
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Iron Trotter")
    title = pygame.image.load("images/titleScreen.png")
    titlerect = title.get_rect()

    mapthing = map.generate_map(1000,1000)

    f = protocol.ClientFactory()
    f.protocol = TrotterSub

    def pyevent():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                reactor.stop()
                #sys.exit()
            elif event.type == pygame.KEYDOWN:
                # --- KEY handlers go HERE ---
                if event.key == pygame.K_m:
                    print "c"
                elif event.key == pygame.K_x:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
        mapthing.draw()
        #screen.blit(title, titlerect)
        pygame.display.flip()


    lc = LoopingCall(pyevent)
    lc.start(0.1)

    reactor.connectTCP(addr, 8000, f)
    reactor.run()


# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()
