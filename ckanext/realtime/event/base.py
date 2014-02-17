''' Base event classes '''
import datetime

class package_event(object):
    '''Event for package(dataset) level data observation'''
    def __init__(self, package_id):
        self.package_id = package_id
        self.timestamp = str(datetime.datetime.now())

class resource_event(object):
    '''Event for resource level data observation'''
    def __init__(self, resource_id):
        self.resource_id = resource_id
        self.timestamp = str(datetime.datetime.now())
