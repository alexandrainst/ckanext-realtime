import ckanext.realtime.event.base as base


class DatastoreCreateEvent(base.package_event, base.resource_event):
    def __init__(self, package_id, resource_id):
        base.package_event.__init__(self, package_id)
        base.resource_event.__init__(self, resource_id)


class DatastoreInsertEvent(base.resource_event):
    def __init__(self, resource_id):
        base.resource_event.__init__(self, resource_id)
 

class DatastoreUpdateEvent(base.resource_event):
    def __init__(self, resource_id):
        base.resource_event.__init__(self, resource_id)


class DatastoreDeleteEvent(base.resource_event):
    def __init__(self, resource_id):
        base.resource_event.__init__(self, resource_id)


class DatastoreSchemaAlteredEvent(base.resource_event):
    def __init__(self, resource_id):
        base.resource_event.__init__(self, resource_id)
