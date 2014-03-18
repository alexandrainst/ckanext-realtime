import ckan.logic
import ckan.tests as tests
from ckanext.realtime.event.event_factory import EventFactory


class TestEventFactory(tests.CheckMethods):
    
    def test_bad_input(self):
        data_dict = {'afgh': 1}
        
        self.assert_raises(ckan.logic.ValidationError,
                          EventFactory.build_events,
                          data_dict)
