import ckanext.realtime.db as db
import ckanext.realtime.event.event_dispatcher as evt
import ckanext.realtime.logic.action as action
import ckanext.realtime.logic.auth as auth

import ckan.plugins as plugins

class RealtimePlugin(plugins.SingletonPlugin):
    '''CKAN Plugin which enables **Observable Datastores** and publishing 
        datastore events.
        
        Enabling ckanext-datastore plugin is a requirement.
    '''
    plugins.implements(plugins.IConfigurable, inherit=True)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IAuthFunctions)
#     plugins.implements(plugins.IDomainObjectModification, inherit=True)
    
    def configure(self, config):
        ''' Configure the plugin - inherited from IConfigurable '''
        
        evt.EventDispatcher.configure(config['ckan.realtime.redis_host'],
                                      config['ckan.realtime.redis_port'])
        
        db.create_datastore_notifier_trigger_function()

    def get_actions(self):
        return {'realtime_broadcast_event': action.realtime_broadcast_event,
                'datastore_make_observable': action.datastore_make_observable,
                'realtime_check_apikey': action.realtime_check_apikey,
                'realtime_check_observable_datastore': action.realtime_check_observable_datastore,
                }
        
    def get_auth_functions(self):
        return {'realtime_broadcast_event': auth.realtime_broadcast_event,
                'datastore_make_observable': auth.datastore_make_observable,
                'realtime_check_apikey': auth.realtime_check_apikey,
                'realtime_check_observable_datastore': auth.realtime_check_observable_datastore,
                }

#     def notify(self, entity, operation):
#         log.debug('domain object modification')
#         log.debug(entity)
#         log.debug(operation)
#         
