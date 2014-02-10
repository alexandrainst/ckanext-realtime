import logging

import ckanext.realtime.db as db
import ckanext.realtime.logic.action as action

import ckan.plugins as plugins

log = logging.getLogger(__name__)

class RealtimePlugin(plugins.SingletonPlugin):
    ''' CKAN Plugin enabling Observable Datastore and thus realtime datastore 
            observation.
        
        This plugin is an extension of ckanext-datastore.
    '''
    
    plugins.implements(plugins.IConfigurable, inherit=True)
    
    def configure(self, config):
        ''' Configure the plugin - inherited from IConfigurable
        
        '''
        self.config = config
        
        self.write_url = self.config['ckan.datastore.write_url']
        
        self._create_metadata_table()

    
    def _create_metadata_table(self):
        ''' 
        ckanext-realtime has some additional metadata on top of the metadata
        in ckanext-datastore.
        '''
        
        create_metadata_table_sql = '''
            CREATE TABLE IF NOT EXISTS _realtime_metadata
            (
                uuid    char(36)    CONSTRAINT firstkey    PRIMARY KEY
            );
        '''
        
        try:
            connection = db._get_engine(
                {'connection_url': self.write_url}).connect()
            connection.execute(create_metadata_table_sql)
        finally:
            connection.close()