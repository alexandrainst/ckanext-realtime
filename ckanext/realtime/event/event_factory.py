import ckanext.realtime.event.datastore as ds_evt
import ckan.logic

_get_or_bust =  ckan.logic.get_or_bust

class EventFactory(object):
    '''Used to build realtime events from data_dict'''
    
    @classmethod
    def build_event(cls, data_dict):
        event_type = _get_or_bust(data_dict, 'event_type')
        
        if event_type == 'datastore_insert':
            return ds_evt.DatastoreInsertEvent(_get_or_bust(data_dict, 
                                                             'resource_id'))
        elif event_type == 'datastore_update':
            return ds_evt.DatastoreUpdateEvent(_get_or_bust(data_dict, 
                                                             'resource_id'))
        elif event_type == 'datastore_delete':
            return ds_evt.DatastoreDeleteEvent(_get_or_bust(data_dict, 
                                                             'resource_id'))
        elif event_type == 'datastore_create':
            return ds_evt.DatastoreCreateEvent(_get_or_bust(data_dict, 
                                                             'package_id'), 
                                                _get_or_bust(data_dict,
                                                             'resource_id'))
        elif event_type == 'datastore_schema_alter':
            return ds_evt.DatastoreSchemaAlterEvent(_get_or_bust(data_dict, 
                                                                  'resource_id'))
        else:
            raise ckan.logic.ValidationError('Bad event_type')
