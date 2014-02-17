import ckanext.realtime.event.datastore as ds_evt

class EventFactory(object):
    
    @classmethod
    def build_events(cls, data_dict):
        if data_dict['event_type'] == 'datastore_insert':
            return [ds_evt.DatastoreInsertEvent(data_dict['resource_id'])]
        elif data_dict['event_type'] == 'datastore_update':
            return [ds_evt.DatastoreUpdateEvent(data_dict['resource_id'])]
        elif data_dict['event_type'] == 'datastore_delete':
            return [ds_evt.DatastoreDeleteEvent(data_dict['resource_id'])]
        else:
            return []
