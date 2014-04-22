'''This module contains ckan API actions specific to ckanext-realtime. 

The docstrings in this module are, for the most part, copied from
ckanext-datastore.

'''
import logging

import ckan.lib.navl.dictization_functions
import ckan.plugins as p
import ckan.model as model
import ckanext.realtime.db as db
from ckanext.realtime.exc import RealtimeError
from ckanext.realtime.event.event_dispatcher import EventDispatcher
from ckanext.realtime.event.event_factory import EventFactory
import ckanext.realtime.logic.schema as realtime_schema

log = logging.getLogger(__name__)
_validate = ckan.lib.navl.dictization_functions.validate


def realtime_broadcast_events(context, data_dict):
    '''Broadcast events to registered listeners.
    
    :param event_type: the type of the event
    :type event_type: string
    :param resource_id: the id of the resource to which the event belongs
        (optional)
    :type resource_id: string
    :param package_id: the id of the package to which the event belongs
        (optional)
    
    '''
    schema = context.get('schema',
                         realtime_schema.realtime_broadcast_events_schema())
    
    data_dict, errors = _validate(data_dict, schema, context)
    if errors:
        raise p.toolkit.ValidationError(errors)
    
    if not 'resource_id' in data_dict and not 'package_id' in data_dict:
        raise p.toolkit.ValidationError('Either resource_id or package_id or both, have to be set')
    
    p.toolkit.check_access('realtime_broadcast_events', context, data_dict)
    
    events = EventFactory.build_events(data_dict)
    EventDispatcher.dispatch(events)


def datastore_make_observable(context, data_dict):
    '''Changes a simple datastore to an observable datastore.
    
    :param resource_id: id of the resource to which the datastore is bound
    :type resource_id: string
    
    '''
    schema = context.get('schema',
                         realtime_schema.datastore_make_observable_schema())
     
    data_dict, errors = _validate(data_dict, schema, context)
    if errors:
        raise p.toolkit.ValidationError(errors)
    
    p.toolkit.check_access('datastore_make_observable', context, data_dict)

    db.add_datastore_notifier_trigger(db.SessionFactory.get_write_engine().url,
                                      data_dict['resource_id'])
    
    
def realtime_check_apikey(context, data_dict):
    schema = context.get('schema',
                         realtime_schema.realtime_check_apikey_schema())
    
    data_dict, errors = _validate(data_dict, schema, context)
    if errors:
        raise p.toolkit.ValidationError(errors)
    
    p.toolkit.check_access('realtime_check_apikey', context, data_dict)
    
    query = model.Session.query(model.User)
    user = query.filter_by(apikey=data_dict['apikey']).first()
    log.info('Checking api key: ' + data_dict['apikey'])
    log.info(user)
    if user:
        return {'auth': True}
    else:
        return {'auth': False}

