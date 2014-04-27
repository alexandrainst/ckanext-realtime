import autobahn.twisted.websocket as ws
from twisted.python import log

import ckanext.realtime.message_handler as ch

class CkanWebSocketServerFactory(ws.WebSocketServerFactory):
    '''Twisted server factory for CKAN WebSocket protocols'''
    
    def __init__(self, url, api_url, apikey, test, debug=False, debugCodePaths=False):
        ws.WebSocketServerFactory.__init__(self, url, debug=debug, 
                                        debugCodePaths=debugCodePaths)
        self.protocol = CkanWebSocketServerProtocol
        self.setProtocolOptions(allowHixie76=True)
        
        if test:
            # most of the responses in the TestClientMessageHandler are mocked
            self.message_handler = ch.TestMessageHandler(api_url, apikey)
        else:
            self.message_handler = ch.MessageHandler(api_url, apikey)
    
    def listen(self):
        '''Listen for incoming WebSocket connections'''
        ws.listenWS(self)
    
    def register(self, client):
        self.message_handler.register_websocket_client(client)
    
    def unregister(self, client):
        self.message_handler.unregister_websocket_client(client)
    
    def handle_from_redis(self, msg):
        self.message_handler.handle_message_from_redis(msg)
    
    def handle_from_client(self, msg, client):
        self.message_handler.handle_message_from_client(msg, client)
    
    
class CkanWebSocketServerProtocol(ws.WebSocketServerProtocol):
    '''CKAN WebSocket protocol'''
    def onOpen(self):
        self.factory.register(self)
    
    def onMessage(self, msg, binary):
        if binary:
            return
        log.msg('request: ' + msg)
        self.factory.handle_from_client(msg, self)
    
    def connectionLost(self, reason):
        ws.WebSocketServerProtocol.connectionLost(self, reason)
        self.factory.unregister(self)
