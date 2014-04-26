import jsonpickle
import requests
import urlparse

SUCCESS_MESSAGE = 'SUCCESS'
FAIL_MESSAGE = 'FAIL'
NON_DATASTORE_MESSAGE = 'NOT-A-DATASTORE'
INVALID_RESOURCE_MESSAGE = 'INVALID-RESOURCE'

class client_message_handler_base(object):
    
    def __init__(self, api_url, apikey):
        self.api_url = api_url
        self.wss_api_key = apikey
    
    def handle_message(self, json_msg):
        '''Handle incoming messages from WebSocket clients
        
        This method should be called invoked through either ClientMessageHandler
         or TestClientMessageHandler.
         
        :param json_msg: json string containing request body that came from client.
        :type json_msg: basestring
        
        '''
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

class ClientMessageHandler(client_message_handler_base):
    '''This class handles the requests from WebSocket clients and gives 
        appropriate responses.
    
    '''
    def _authenticate(self, request):
        if self._check_apikey(request['apikey_to_check']):
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
        pass

    def _datastore_unsubscribe(self, request):
        pass


class TestClientMessageHandler(client_message_handler_base):
    '''Mock API of ClientMessageHandler for testing purposes'''
    
    def _authenticate(self, request):
        if request['apikey_to_check'] == 'correctKey':
            return {'type': 'auth', 'result': True}
        else:
            return {'type': 'auth', 'result': False}

    def _datastore_subscribe(self, request):
        if request['resource_id'] == 'observableResource':
            return {'type': 'datastoresubscribe', 'resource_id': request['resource_id'], 'result': SUCCESS_MESSAGE}
        elif request['resource_id'] == 'nonObservableResource':
            return {'type': 'datastoresubscribe', 'resource_id': request['resource_id'], 'result': FAIL_MESSAGE}
        elif request['resource_id'] == 'nonDatastoreResource':
            return {'type': 'datastoresubscribe', 'resource_id': request['resource_id'], 'result': NON_DATASTORE_MESSAGE}
        elif request['resource_id'] == 'invalidResource':
            return {'type': 'datastoresubscribe', 'resource_id': request['resource_id'], 'result': INVALID_RESOURCE_MESSAGE}
        else:
            return None

    def _datastore_unsubscribe(self, request):
        if request['resource_id'] == 'observableResource':
            return {'type': 'datastoreunsubscribe', 'resource_id': request['resource_id'], 'result': SUCCESS_MESSAGE}
        elif request['resource_id'] == 'nonObservableResource':
            return {'type': 'datastoreunsubscribe', 'resource_id': request['resource_id'], 'result': FAIL_MESSAGE}
        elif request['resource_id'] == 'nonDatastoreResource':
            return {'type': 'datastoreunsubscribe', 'resource_id': request['resource_id'], 'result': NON_DATASTORE_MESSAGE}
        elif request['resource_id'] == 'invalidResource':
            return {'type': 'datastoreunsubscribe', 'resource_id': request['resource_id'], 'result': INVALID_RESOURCE_MESSAGE}
        else:
            return None
