from twisted.internet import reactor    #could use GeventReactor
# from twisted.python import log

from autobahn.twisted.websocket import WebSocketServerFactory, WebSocketServerProtocol, \
    listenWS

class CkanWebsocketServerFactory(WebSocketServerFactory):
    '''
    Handler for Websocket clients with autobahn WebSocket server.
    '''
    def __init__(self, url, debug=False, debugCodePaths=False):
        WebSocketServerFactory.__init__(self, url, debug=debug, debugCodePaths=debugCodePaths)
        self.clients = []
        self.tickcount = 0
        self.tick()
    
    def start(self):
        self.protocol = CkanWebsocketServerProtocol
        self.setProtocolOptions(allowHixie76=True)
        listenWS(self)

        reactor.run()
    
    def tick(self):
        self.tickcount += 1
        self.broadcast("tick %d from server" % self.tickcount)
        reactor.callLater(1, self.tick)
    
    def register(self, client):
        if not client in self.clients:
            print("registered client {}".format(client.peer))
            self.clients.append(client)
    
    def unregister(self, client):
        if client in self.clients:
            print("unregistered client {}".format(client.peer))
            self.clients.remove(client)

            
    def broadcast(self, msg):
        print("broadcasting message '{}' ..".format(msg))
        for c in self.clients:
            c.sendMessage(msg.encode('utf8'))
            print("message sent to {}".format(c.peer))
        
        
class CkanWebsocketServerProtocol(WebSocketServerProtocol):
    '''
    Websocket client representkation.
    '''
    def onOpen(self):
        self.factory.register(self)

    def onMessage(self, msg, binary):
        if binary:
            return
        print msg
        self.sendMessage('good day to you madam')

    def connectionLost(self, reason):
        WebSocketServerProtocol.connectionLost(self, reason)
        self.factory.unregister(self)
