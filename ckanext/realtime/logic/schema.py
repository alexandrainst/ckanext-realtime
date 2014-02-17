import ckan.plugins as p

_get_validator = p.toolkit.get_validator

_not_missing = _get_validator('not_missing')
_not_empty = _get_validator('not_empty')
_resource_id_exists = _get_validator('resource_id_exists')
_package_id_exists = _get_validator('package_id_exists')
_ignore_missing = _get_validator('ignore_missing')


def realtime_broadcast_events_schema():
    schema = {
              'event_type': [_not_empty, unicode],
              'package_id': [_ignore_missing, unicode, _package_id_exists],
              'resource_id': [_ignore_missing, unicode, _resource_id_exists],
              }
    

    return schema


def datastore_make_observable_schema():
    schema = {
              'resource_id': [_not_empty, unicode, _resource_id_exists],
              }
    return schema