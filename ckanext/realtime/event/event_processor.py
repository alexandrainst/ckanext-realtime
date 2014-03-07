import redis
import jsonpickle

class EventProcessor(object):
    '''Used by event listener nodes in order to receive events from Redis
    
    TODO: write unit tests
    
    '''
    def __init__(self, redis_host, redis_port, event_processor_func):
        self.event_processor_func = event_processor_func
        self.r = redis.StrictRedis(host=redis_host, port=redis_port, db=0)
        self.pubsub = self.r.pubsub()

    def run(self):
        for event in self.pubsub.listen():
            if not isinstance(event['data'], basestring):
                continue
            obj = jsonpickle.decode(event['data'])
            self.event_processor_func(obj)

    def subscribe(self, event_classes):
        '''Subscribe to specific type of events
        
        :param event_classes: list of event classes, extending one of interfaces
            in the ckanext.realtime.event.base module
        :type event_classes: list
        
        '''
        channels = []
        for ec in event_classes:
            channels.append(ec.channel_name)
        
        self.pubsub.subscribe(channels)
