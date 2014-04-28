import paste.fixture
import pylons.test
import pylons.config as config
import sqlalchemy
import sqlalchemy.orm as orm

import ckan.model as model
import ckan.plugins as p
import ckan.lib.create_test_data as ctd
from ckanext.datastore.tests.helpers import rebuild_all_dbs, set_url_type

import ckan.tests as tests

import ckanext.realtime as rt


class TestRealtimeActions(object):
    ''' Tests for actions ckanext.realtime.logic.action module
    '''
    sysadmin_user = None
    normal_user = None
    
    @classmethod
    def setup_class(cls):
        '''Nose runs this method once to setup our test class.'''        
        # Make the Paste TestApp that we'll use to simulate HTTP requests to
        # CKAN.
        cls.app = paste.fixture.TestApp(pylons.test.pylonsapp)

        
        engine = sqlalchemy.create_engine(config['ckan.datastore.write_url'])
        cls.Session = orm.scoped_session(orm.sessionmaker(bind=engine))
        
        rebuild_all_dbs(cls.Session)
        p.load('datastore')
        p.load('realtime')
        
        ctd.CreateTestData.create()
        
        cls.sysadmin_user = model.User.get('testsysadmin')
        cls.normal_user = model.User.get('annafan')
        
        # make test resource writable through action api
        set_url_type(
            model.Package.get('annakarenina').resources, cls.sysadmin_user)
        
        cls._create_test_datastore()

    
    @classmethod
    def _create_test_datastore(cls):
        resource = model.Package.get('annakarenina').resources[0]
        tests.call_action_api(cls.app, 'datastore_create',
                              resource_id=resource.id,
                              apikey=cls.sysadmin_user.apikey)

    @classmethod
    def teardown_class(cls):
        '''Nose runs this method once after all the test methods in our class
        have been run.
        '''
        rebuild_all_dbs(cls.Session)
        
        # unload plugins
        p.unload('datastore')
        p.unload('realtime')
    
    # realtime_make_observable tests    
    def test_make_observable_by_admin(self):
        resource = model.Package.get('annakarenina').resources[0]
  
        tests.call_action_api(self.app, 'datastore_make_observable',
                              resource_id=resource.id,
                              apikey=self.sysadmin_user.apikey)
 
    def test_make_observable_by_normal_user(self):
        # should it really be 409?
        resource = model.Package.get('annakarenina').resources[0]
   
        tests.call_action_api(self.app, 'datastore_make_observable',
                              resource_id=resource.id,
                              apikey=self.normal_user.apikey,
                              status=409)
           
    def test_make_observable_without_apikey(self):
        resource = model.Package.get('annakarenina').resources[0]
        tests.call_action_api(self.app, 'datastore_make_observable',
                              resource_id=resource.id,
                              status=403)
        
    def test_make_observable_by_admin_bad_request(self):
        tests.call_action_api(self.app, 'datastore_make_observable',
                              apikey=self.sysadmin_user.apikey,
                              status=409)
    
    # realtime_broadcast_events tests           
    def test_broadcast_event_by_admin(self):
        resource = model.Package.get('annakarenina').resources[0]
  
        tests.call_action_api(self.app, 'realtime_broadcast_event',
                              resource_id=resource.id,
                              event_type='datastore_update',
                              apikey=self.sysadmin_user.apikey)
 
    def test_broadcast_event_by_normal_user(self):
        # should it really be 409?
        resource = model.Package.get('annakarenina').resources[0]
   
        tests.call_action_api(self.app, 'realtime_broadcast_event',
                              resource_id=resource.id,
                              event_type='datastore_update',
                              apikey=self.normal_user.apikey,
                              status=409)
           
    def test_broadcast_event_without_apikey(self):
        resource = model.Package.get('annakarenina').resources[0]
        tests.call_action_api(self.app, 'realtime_broadcast_event',
                              resource_id=resource.id,
                              event_type='datastore_update',
                              status=403)
        
    def test_broadcast_event_by_admin_bad_request(self): 
        tests.call_action_api(self.app, 'realtime_broadcast_event',
                              event_type='datastore_update',
                              apikey=self.sysadmin_user.apikey,
                              status=409)
    
    # realtime_check_apikey tests    
    def test_check_apikey_by_admin(self):
        res = tests.call_action_api(self.app, 'realtime_check_apikey',
                                    apikey_to_check=self.normal_user.apikey,
                                    apikey=self.sysadmin_user.apikey)
        
        assert res['exists']
    
    def test_check_invalid_apikey_by_admin(self):
        res = tests.call_action_api(self.app, 'realtime_check_apikey',
                                    apikey_to_check='invalidkey',
                                    apikey=self.sysadmin_user.apikey)
        
        assert not res['exists']
    
    def test_check_apikey_by_normal_user(self):
        tests.call_action_api(self.app, 'realtime_check_apikey',
                                    apikey_to_check=self.sysadmin_user.apikey,
                                    apikey=self.normal_user.apikey,
                                    status=409)
    
    def test_check_apikey_without_apikey(self):
        tests.call_action_api(self.app, 'realtime_check_apikey',
                                    apikey_to_check=self.sysadmin_user.apikey,
                                    status=403)
        
    # realtime_check_observable_datastore tests
    def test_check_observable_datastore_by_admin(self):
        resource = model.Package.get('annakarenina').resources[0]
        
        # make observable
        tests.call_action_api(self.app, 'datastore_make_observable',
                              resource_id=resource.id,
                              apikey=self.sysadmin_user.apikey)
        
        # is observable?
        res = tests.call_action_api(self.app, 'realtime_check_observable_datastore',
                                    resource_id=resource.id,
                                    apikey=self.sysadmin_user.apikey)
        
        assert res['is_observable'] == rt.YES_MESSAGE
    
    def test_check_observable_datastore_by_normal_user(self):
        resource = model.Package.get('annakarenina').resources[0]
        # is observable?
        tests.call_action_api(self.app, 'realtime_check_observable_datastore',
                                    resource_id=resource.id,
                                    apikey=self.normal_user.apikey,
                                    status=409)
    
    def test_check_observable_datastore_without_apikey(self):
        resource = model.Package.get('annakarenina').resources[0]
        # is observable?
        tests.call_action_api(self.app, 'realtime_check_observable_datastore',
                                    resource_id=resource.id,
                                    status=403)
        
    def test_check_observable_datastore_by_admin_bad_request(self):
        # is observable?
        tests.call_action_api(self.app, 'realtime_check_observable_datastore',
                                    apikey=self.sysadmin_user.apikey,
                                    status=409)
    
    def test_check_normal_datastore(self):
        package = model.Package.get('annakarenina')
        
        # create new resource
        res = tests.call_action_api(self.app, 'datastore_create',
                                    resource={'package_id': package.id},
                                    url='foo',
                                    apikey=self.sysadmin_user.apikey)
        
        # is observable?
        res = tests.call_action_api(self.app, 'realtime_check_observable_datastore',
                                    resource_id=res['resource_id'],
                                    apikey=self.sysadmin_user.apikey)
        
        assert res['is_observable'] == rt.NO_MESSAGE
    
    def test_check_non_datastore(self):
        package = model.Package.get('annakarenina')
        
        # create new resource
        res = tests.call_action_api(self.app, 'resource_create',
                                    package_id=package.id,
                                    url='foo',
                                    apikey=self.sysadmin_user.apikey)
        
        # is observable?
        res = tests.call_action_api(self.app, 'realtime_check_observable_datastore',
                                    resource_id=res['id'],
                                    apikey=self.sysadmin_user.apikey)
        
        assert res['is_observable'] == rt.NON_DATASTORE_MESSAGE
    
    
    def test_invalid_resource(self):
        # in observable?
        tests.call_action_api(self.app, 'realtime_check_observable_datastore',
                                    resource_id='invalidResource',
                                    apikey=self.sysadmin_user.apikey,
                                    status=409)
