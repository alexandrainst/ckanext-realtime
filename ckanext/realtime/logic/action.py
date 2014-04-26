'''This module contains ckan API actions specific to ckanext-realtime. 

The docstrings in this module are, for the most part, copied from
ckanext-datastore.

'''
import logging
import pylons
import sqlalchemy

import ckan.lib.navl.dictization_functions
import ckan.plugins as p
import ckan.model as model
import ckanext.realtime as rt
import ckanext.realtime.db as db
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

    db.add_datastore_notifier_trigger(data_dict['resource_id'])
    
    
def realtime_check_apikey(context, data_dict):
    '''Check whether a particular apikey exists.
    
    :param apikey_to_check: target apikey
    :type api_key_to_check: string
    
    :return: whether the apikey exists
    :rtype: dictionary
    
    '''
    schema = context.get('schema',
                         realtime_schema.realtime_check_apikey_schema())
    
    data_dict, errors = _validate(data_dict, schema, context)
    if errors:
        raise p.toolkit.ValidationError(errors)
    
    p.toolkit.check_access('realtime_check_apikey', context, data_dict)
    
    query = model.Session.query(model.User)
    user = query.filter_by(apikey=data_dict['apikey_to_check']).first()
    log.info('Checking api key: ' + data_dict['apikey_to_check'])
    log.info(user)
    if user:
        return {'exists': True}
    else:
        return {'exists': False}
    
    
def realtime_check_observable_datastore(context, data_dict):
    '''Check whether a particular datastore is observable
    
    :param resource_id: target resource
    :type resource_id: string
    
    :return: indication whether the resource is an observable datastore, 
        non-observable datastore or not a datastore
    :rtype: dictionary
        
    '''
    schema = context.get('schema', realtime_schema.realtime_check_observable_datastore_schema())
    data_dict, errors = _validate(data_dict, schema, context)
    if errors:
        raise p.toolkit.ValidationError(errors)
    
    p.toolkit.check_access('realtime_check_observable_datastore', context, data_dict)
    
    if not _datastore_exists(data_dict):
        return {'is_observable': rt.NON_DATASTORE_MESSAGE}
    elif db.notifier_trigger_function_exists(data_dict['resource_id']):
        return {'is_observable': rt.YES_MESSAGE}
    else:
        return {'is_observable': rt.NO_MESSAGE}


def _datastore_exists(data_dict):
    connection_url = pylons.config['ckan.datastore.write_url']

    res_id = data_dict['resource_id']
    resources_sql = sqlalchemy.text(u'''SELECT 1 FROM "_table_metadata"
                                        WHERE name = :id AND alias_of IS NULL''')
    
    engine = sqlalchemy.create_engine(connection_url)
    
    results = engine.execute(resources_sql, id=res_id)
    return results.rowcount > 0

