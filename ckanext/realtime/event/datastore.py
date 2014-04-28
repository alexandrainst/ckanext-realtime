import ckanext.realtime.event.base as base


class DatastoreCreateEvent(base.package_event, base.resource_event):
    '''Fired when a new datastore is created
    
    TODO: emiting not implemented
    
    '''
    event_name = 'datastore_create'
    
    def __init__(self, package_id, resource_id):
        base.package_event.__init__(self, package_id)
        base.resource_event.__init__(self, resource_id)


class DatastoreInsertEvent(base.resource_event):
    '''Fired for each new tuple inserted in a particular observable datastore'''
    event_name = 'datastore_insert'
    
    def __init__(self, resource_id):
        base.resource_event.__init__(self, resource_id)


class DatastoreUpdateEvent(base.resource_event):
    '''Fired for each updated tuple in a particular observable datastore'''
    event_name = 'datastore_update'
    
    def __init__(self, resource_id):
        base.resource_event.__init__(self, resource_id)


class DatastoreDeleteEvent(base.resource_event):
    '''Fired for each deleted tuple in a particular observable datastore'''
    event_name = 'datastore_delete'
    
    def __init__(self, resource_id):
        base.resource_event.__init__(self, resource_id)


class DatastoreSchemaAlterEvent(base.resource_event):
    '''Fired when the structure of some datastore is changed
    
    TODO: emiting not implemented
    
    '''
    event_name = 'datastore_schema_alter'
    
    def __init__(self, resource_id):
        base.resource_event.__init__(self, resource_id)
