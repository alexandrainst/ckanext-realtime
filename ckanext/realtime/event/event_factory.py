import ckanext.realtime.event.datastore as ds_evt
import ckan.logic

_get_or_bust =  ckan.logic.get_or_bust

class EventFactory(object):
    
    @classmethod
    def build_events(cls, data_dict):
        event_type = _get_or_bust(data_dict, 'event_type')
        
        if event_type == 'datastore_insert':
            return [ds_evt.DatastoreInsertEvent(_get_or_bust(data_dict, 
                                                             'resource_id'))]
        elif event_type == 'datastore_update':
            return [ds_evt.DatastoreUpdateEvent(_get_or_bust(data_dict, 
                                                             'resource_id'))]
        elif event_type == 'datastore_delete':
            return [ds_evt.DatastoreDeleteEvent(_get_or_bust(data_dict, 
                                                             'resource_id'))]
        else:
            return []
