'''Base event classes'''
import datetime

class package_event(object):
    '''Event for package(dataset) level data observation'''
    def __init__(self, package_id):
        '''
        :param package_id: the dataset to which the event is related
        :type package_id: string
        
        '''
        self.package_id = package_id
        self.timestamp = str(datetime.datetime.now())

    def __repr__(self):
        return ("{0}(package_id='{1}', timestamp='{2}')"
                .format(self.__class__, self.package_id, self.timestamp))


class resource_event(object):
    '''Event for resource level data observation'''
    def __init__(self, resource_id):
        '''
        :param resource_id: the resource to which the event is related
        :type resource_id: string
        
        '''
        self.resource_id = resource_id
        self.timestamp = str(datetime.datetime.now())
        
    def __repr__(self):
        return ("{0}(resource_id='{1}', timestamp='{2}')"
                .format(self.__class__, self.resource_id, self.timestamp))
