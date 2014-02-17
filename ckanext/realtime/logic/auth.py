'''Authorization for ckan api actions exposed by ckanext-realtime'''

import ckan.plugins as p


def realtime_auth(context, data_dict, privilege='resource_update'):
    if not 'id' in data_dict:
        data_dict['id'] = data_dict.get('resource_id')
    user = context.get('user')

    authorized = p.toolkit.check_access(privilege, context, data_dict)

    if not authorized:
        return {
            'success': False,
            'msg': p.toolkit._('User {0} not authorized to update resource {1}'
                    .format(str(user), data_dict['id']))
        }
    else:
        return {'success': True}


def realtime_broadcast_events(context, data_dict):
    return realtime_auth(context, data_dict)


def datastore_make_observable(context, data_dict):
    return realtime_auth(context, data_dict)

