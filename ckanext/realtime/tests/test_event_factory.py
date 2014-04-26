import uuid
import ckan.logic
import ckan.tests as tests
import ckanext.realtime.event.datastore as evt
from ckanext.realtime.event.event_factory import EventFactory


class TestEventFactory(tests.CheckMethods):
    
    def test_bad_input(self):
        data_dict = {'afgh': 1}
        self.assert_raises(ckan.logic.ValidationError,
                           EventFactory.build_events,
                           data_dict)
        
        data_dict = {'event_type': 'foobar', 'resource_id': str(uuid.uuid4())}
        self.assert_raises(ckan.logic.ValidationError,
                           EventFactory.build_events,
                           data_dict)
    
    def test_datastore_create(self):
        data_dict = {'event_type': 'datastore_create', 
                     'resource_id': str(uuid.uuid4()),
                     'package_id': str(uuid.uuid4())}
        
        events = EventFactory.build_events(data_dict)
        
        self.assert_true(isinstance(events[0], evt.DatastoreCreateEvent))
        
    def test_datastore_schema_alter(self):
        data_dict = {'event_type': 'datastore_schema_alter',
                     'resource_id': str(uuid.uuid4())}
        
        events = EventFactory.build_events(data_dict)
        
        self.assert_true(isinstance(events[0], evt.DatastoreSchemaAlterEvent))
        
    def test_datastore_insert(self):
        data_dict = {'event_type': 'datastore_insert', 'resource_id': str(uuid.uuid4())}
        
        events = EventFactory.build_events(data_dict)
        self.assert_true(isinstance(events[0], evt.DatastoreInsertEvent))
    
    def test_datastore_update_event(self):
        data_dict = {'event_type': 'datastore_update', 'resource_id': str(uuid.uuid4())}
        
        events = EventFactory.build_events(data_dict)
        self.assert_true(isinstance(events[0], evt.DatastoreUpdateEvent))
    
    def test_datastore_delete_event(self):
        data_dict = {'event_type': 'datastore_delete', 'resource_id': str(uuid.uuid4())}
        
        events = EventFactory.build_events(data_dict)
        self.assert_true(isinstance(events[0], evt.DatastoreDeleteEvent))
