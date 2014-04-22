import logging

import ckanext.realtime.db as db
import ckanext.realtime.event.event_dispatcher as evt
import ckanext.realtime.logic.action as action
import ckanext.realtime.logic.auth as auth

import ckan.plugins as plugins

log = logging.getLogger(__name__)

class RealtimePlugin(plugins.SingletonPlugin):
    ''' CKAN Plugin enabling Observable Datastore and thus realtime datastore 
            observation.
        
        This plugin builds upon ckanext-datastore.
    '''
    plugins.implements(plugins.IConfigurable, inherit=True)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IAuthFunctions)
#     plugins.implements(plugins.IDomainObjectModification, inherit=True)
    
    def configure(self, config):
        ''' Configure the plugin - inherited from IConfigurable '''
        self.config = config
        
        # from datastore settings
        self.read_url = self.config['ckan.datastore.read_url']
        self.write_url = self.config['ckan.datastore.write_url']
        
        db.SessionFactory.configure(self.read_url, self.write_url)
        evt.EventDispatcher.configure('127.0.0.1', 6379)
        
        db.create_datastore_notifier_trigger_function(self.write_url)

    def get_actions(self):
        return {'realtime_broadcast_events': action.realtime_broadcast_events,
                'datastore_make_observable': action.datastore_make_observable,
                'realtime_check_apikey': action.realtime_check_apikey,
                }
        
    def get_auth_functions(self):
        return {'realtime_broadcast_events': auth.realtime_broadcast_events,
                'datastore_make_observable': auth.datastore_make_observable,
                'realtime_check_apikey': auth.realtime_check_apikey,
                }

#     def notify(self, entity, operation):
#         log.debug('domain object modification')
#         log.debug(entity)
#         log.debug(operation)
#         
