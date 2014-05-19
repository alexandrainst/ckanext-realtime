from twisted.internet import reactor, protocol
from twisted.python import log

from txredis.client import RedisSubscriber

def connect_event_processor(redis_host, redis_port, 
                            websocket_factory, events_for_subscribing):
    '''Initiate connection to Redis process.
    
    :param redis_host: the address of redis server
    :type redis_host: basestring
    :param redis_port: port on which the redis server in listening
    :type redis_port: int
    :param websocket_factory: twisted server factory for creating 
        WS protocols of ckanext-realtime
    :type websocket_factory: ckanext.realtime.twisted.websocket.CKANWebSocketServerFactory
    
    '''
    
    client_creator = protocol.ClientCreator(reactor, 
                                            CkanEventProcessorProtocol,
                                            websocket_factory)
    
    d = client_creator.connectTCP(redis_host, redis_port)
    d.addCallback(_connection_success, *events_for_subscribing)
    d.addErrback(_connection_failure)
    
    return d


def _connection_success(event_processor, *event_classes):
    '''Callback to deferred event_processor connection process'''
    event_processor.subscribe(event_classes)


def _connection_failure(error):
    '''Errback to deferred event_processor connection process'''
    log.err(error)


class CkanEventProcessorProtocol(RedisSubscriber):
    '''txredis-powered subscriber for receiving realtime events from CKAN'''
    
    def __init__(self, websocket_factory):
        RedisSubscriber.__init__(self)
        self.websocket_factory = websocket_factory

    def subscribe(self, event_classes):
        '''Subscribe to specific type of events
        
        :param event_classes: list of event classes, extending one of interfaces
            in the ckanext.realtime.event.base module
        :type event_classes: list
        
        '''
        channels = [ec.event_name for ec in event_classes]
        RedisSubscriber.subscribe(self, *channels)
        log.msg('subscribed to {} new channels'.format(len(channels)))
        
    def messageReceived(self, channel, message):
        '''Pass the received CKAN events to WSS to be sent to WSCs'''
        
        if isinstance(message, basestring):
            self.websocket_factory.handle_from_redis(message)
