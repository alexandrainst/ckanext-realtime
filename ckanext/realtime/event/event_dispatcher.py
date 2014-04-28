import jsonpickle
import logging
import redis

log = logging.getLogger(__name__)


class EventDispatcher(object):
    '''Mediates events from ckan API actions to subscribers'''
    
    @classmethod
    def configure(cls, redis_host, redis_port):
        cls.r = redis.StrictRedis(host=redis_host, port=redis_port, db=0)
    
    @classmethod
    def dispatch_one(cls, event):
        cls.r.publish(event.event_name, jsonpickle.encode(event))
            
    @classmethod
    def dispatch(cls, events):
        for e in events:
            cls.dispatch_one(e)
