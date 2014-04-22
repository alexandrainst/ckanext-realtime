import jsonpickle
import requests
import urlparse

class ClientMessageHandler(object):
    
    def __init__(self, api_url, apikey, test):
        self.api_url = api_url
        self.wss_api_key = apikey
        self.test = test
    
    def handle_message(self, json_msg):
        request = jsonpickle.decode(json_msg)
        response = None
        if request['type'] == 'auth':
            response = self._authenticate(request)
        elif request['type'] == 'datastoresubscribe':
            response = self._datastore_subscribe(request)
        elif request['type'] == 'datastoreunsubscribe':
            response = self._datastore_unsubscribe(request)
        if response:
            response = jsonpickle.encode(response)
            
        return response
    
    def _authenticate(self, request):
        if not self.test and self._check_apikey(request['apikey']):
            return {'type': 'auth', 'result': True}
        elif self.test and request['apikey'] == 'correctKey':
            return {'type': 'auth', 'result': True}
        else:
            return {'type': 'auth', 'result': False}
    
    def _check_apikey(self, apikey):
        # FIXME: should we encrypt the api_key of the client?
        
        # make a call to the CKAN API to see if the provided apikey is valid
        url = urlparse.urljoin(self.api_url, 'realtime_check_apikey')
        payload = {'apikey': apikey}
        r = requests.post(url,
                          data=jsonpickle.encode(payload),
                          headers={'Authorization': self.wss_api_key,
                                   'Content-Type': 'application/json'})
        
        # read response from the CKAN API
        response = jsonpickle.decode(r.text)
        if response['result']['auth']:
            return True
        return False
    
    def _datastore_subscribe(self, request):
        if not self.test:
            pass
        elif self.test:
            if request['resource_id'] == 'observableResource':
                return {'type': 'datastoresubscribe', 'resource_id': request['resource_id'], 'result': 'SUCCESS'}
            elif request['resource_id'] == 'nonObservableResource':
                return {'type': 'datastoresubscribe', 'resource_id': request['resource_id'], 'result': 'FAIL'}
            elif request['resource_id'] == 'nonDatastoreResource':
                return {'type': 'datastoresubscribe', 'resource_id': request['resource_id'], 'result': 'NOT-A-DATASTORE'}
            elif request['resource_id'] == 'invalidResource':
                return {'type': 'datastoresubscribe', 'resource_id': request['resource_id'], 'result': 'INVALID-RESOURCE'}
            else:
                return None

    def _datastore_unsubscribe(self, request):
        if not self.test:
            pass
        elif self.test:
            if request['resource_id'] == 'observableResource':
                return {'type': 'datastoreunsubscribe', 'resource_id': request['resource_id'], 'result': 'SUCCESS'}
            elif request['resource_id'] == 'nonObservableResource':
                return {'type': 'datastoreunsubscribe', 'resource_id': request['resource_id'], 'result': 'FAIL'}
            elif request['resource_id'] == 'nonDatastoreResource':
                return {'type': 'datastoreunsubscribe', 'resource_id': request['resource_id'], 'result': 'NOT-A-DATASTORE'}
            elif request['resource_id'] == 'invalidResource':
                return {'type': 'datastoreunsubscribe', 'resource_id': request['resource_id'], 'result': 'INVALID-RESOURCE'}
            else:
                return None
