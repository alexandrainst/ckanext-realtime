import autobahn.twisted.websocket as ws
from twisted.python import log

from ckanext.realtime.client_handler import ClientMessageHandler

class CkanWebSocketServerFactory(ws.WebSocketServerFactory):
    '''Twisted server factory for CKAN WebSocket protocols'''
    
    def __init__(self, url, api_url, apikey, test, debug=False, debugCodePaths=False):
        ws.WebSocketServerFactory.__init__(self, url, debug=debug, 
                                        debugCodePaths=debugCodePaths)
        self.clients = []
        self.protocol = CkanWebSocketServerProtocol
        self.setProtocolOptions(allowHixie76=True)
        self.client_handler = ClientMessageHandler(api_url, apikey, test)
    
    def listen(self):
        '''Listen for incoming WebSocket connections'''
        ws.listenWS(self)
    
    def register(self, client):
        if not client in self.clients:
            log.msg("registered client {}".format(client.peer))
            self.clients.append(client)
    
    def unregister(self, client):
        if client in self.clients:
            log.msg("unregistered client {}".format(client.peer))
            self.clients.remove(client)
    
    def broadcast(self, msg):
        log.msg("broadcasting message '{}' ..".format(msg))
        for c in self.clients:
            c.sendMessage(msg.encode('utf8'))
            log.msg("message sent to {}".format(c.peer))
            
    def handle_message(self, msg):
        return self.client_handler.handle_message(msg)
    
    
class CkanWebSocketServerProtocol(ws.WebSocketServerProtocol):
    '''CKAN WebSocket protocol'''
    def onOpen(self):
        self.factory.register(self)
    
    def onMessage(self, msg, binary):
        if binary:
            return
        log.msg('request: ' + msg)
        
        result = self.factory.handle_message(msg)
        log.msg(result)
        if result and isinstance(result, basestring):
            log.msg('response: ' + result)
            self.sendMessage(result)
    
    def connectionLost(self, reason):
        ws.WebSocketServerProtocol.connectionLost(self, reason)
        self.factory.unregister(self)
