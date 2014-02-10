import paste.fixture
import pylons.test
import pylons.config as config
import sqlalchemy.orm as orm

import ckan.model as model
import ckan.plugins as p
import ckan.lib.create_test_data as ctd
from ckanext.datastore.tests.helpers import rebuild_all_dbs, set_url_type

import ckanext.realtime.db as db

import ckan.tests as tests


class TestRealtimeCreateActions(object):
    ''' Tests for create actions ckanext.realtime.logic.action module
    '''
    sysadmin_user = None
    normal_user = None
    
    @classmethod
    def setup_class(cls):
        '''Nose runs this method once to setup our test class.'''        

        # Make the Paste TestApp that we'll use to simulate HTTP requests to
        # CKAN.
        cls.app = paste.fixture.TestApp(pylons.test.pylonsapp)

        p.load('datastore')
        p.load('realtime')
        
        ctd.CreateTestData.create()
        
        cls.sysadmin_user = model.User.get('testsysadmin')
        cls.normal_user = model.User.get('annafan')
        
        engine = db._get_engine(config['ckan.datastore.write_url'])
        cls.Session = orm.scoped_session(orm.sessionmaker(bind=engine))
        
        # make test resource writable through action api
        set_url_type(
            model.Package.get('annakarenina').resources, cls.sysadmin_user)
        

    
    @classmethod
    def teardown_class(cls):
        '''Nose runs this method once after all the test methods in our class
        have been run.
        '''
#         rebuild_all_dbs(cls.Session)
        
        # unload plugins
        p.unload('realtime')
        p.unload('datastore')
    

        
    def test_create_observable_ds_by_admin_succeeds(self):
        resource = model.Package.get('annakarenina').resources[0]

        tests.call_action_api(self.app, 'observable_datastore_create', resource_id=resource.id,
                              apikey=self.sysadmin_user.apikey)
        
    def test_create_observable_ds_by_normal_user_succeeds(self):
        resource = model.Package.get('annakarenina').resources[0]
 
        tests.call_action_api(self.app, 'observable_datastore_create', resource_id=resource.id,
                              apikey=self.normal_user.apikey)
         
         
    def test_create_observable_ds_without_apikey_fails(self):
        resource = model.Package.get('annakarenina').resources[0]
        tests.call_action_api(self.app, 'observable_datastore_create', 
                              resource_id=resource.id,
                              status=403)
