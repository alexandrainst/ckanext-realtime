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
        
        if response:
            response = jsonpickle.encode(response)
        else:
            return 'good day to you madam'
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
