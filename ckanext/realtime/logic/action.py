import logging

import ckanext.realtime.db as db
import ckan.plugins as p

from ckanext.realtime.exc import RealtimeError

log = logging.getLogger(__name__)

def observable_datastore_create(context, data_dict):
    ''' Initiates Observable Datastore
    
    This action is based upon *datastore_create* action in the datastore extension.
    
    :param resource_id: resource id that the data is going to be stored against.
    :type resource_id: string
    :param aliases: names for read only aliases of the resource. (optional)
    :type aliases: list or comma separated string
    :param fields: fields/columns and their extra metadata. (optional)
    :type fields: list of dictionaries
    :param records: the data, eg: [{"dob": "2005", "some_stuff": ["a", "b"]}]  (optional)
    :type records: list of dictionaries
    :param primary_key: fields that represent a unique key (optional)
    :type primary_key: list or comma separated string
    :param indexes: indexes on table (optional)
    :type indexes: list or comma separated string
    
    :returns: The newly created data object.
    :rtype: dictionary
    '''
    # No need to validate odatastore against different schema
    # No need to create a separate auth function
    result = p.toolkit.get_action('datastore_create')(context, data_dict)
    
    # Do the observable datastore creation specific things here
    # do we need to have some extra metadata for odatastores?
    # for starters, should just mark datastores as observable
    success = db.mark_as_observable(data_dict['resource_id'])
    if not success:
        raise RealtimeError('Marking the datastore as observable failed')
    
    log.info('Observable Datastore Created.')
    
    return result