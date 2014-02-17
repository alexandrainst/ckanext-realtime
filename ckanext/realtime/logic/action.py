'''This module contains ckan API actions specific to ckanext-realtime. 

The docstrings in this module are, for the most part, copied from
ckanext-datastore.

'''
import logging

import ckanext.realtime.db as db
from ckanext.realtime.exc import RealtimeError
from ckanext.realtime.event.event_dispatcher import EventDispatcher
from ckanext.realtime.event.event_factory import EventFactory

log = logging.getLogger(__name__)


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
    events = EventFactory.build_events(data_dict)
    EventDispatcher.dispatch(events)


def datastore_make_observable(context, data_dict):
    '''Changes a simple datastore to an observable datastore.
    
    :param resource_id: id of the resource to which the datastore is bound
    :type resource_id: string
    
    '''
    success = db.insert_observable_datastore_metadata(data_dict['resource_id'])
    if not success:
        raise RealtimeError('Marking the datastore as observable failed')

    db.add_datastore_notifier_trigger(db.SessionFactory.get_write_engine().url,
                                      data_dict['resource_id'])

