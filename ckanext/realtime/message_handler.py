from __future__ import absolute_import
import jsonpickle
import requests
import urlparse

from twisted.python import log

import ckanext.realtime as rt

class message_handler_base(object):
    '''This class contains the logic for handling messages from WebSocket clients
        and Redis subscriber. You should use 1 of it's derived classes:
        MessageHandler or TestMessageHandler.
        
    '''

    def __init__(self, api_url, apikey):
        self.api_url = api_url
        self.wss_api_key = apikey
        self.resource_to_clients = {}
        
    def register_websocket_client(self, client):
        '''Register WebSocket client so that it can receive 
            messages from CKAN
            
        :param client: WebSocket client
        :type client: ckanext.realtime.twisted.websocket.CkanWebSocketServerProtocol
        
        '''
        log.msg("register client {}".format(client.peer))
    
    def unregister_websocket_client(self, client):
        ''' Unregister WebSocket client
        
        :param client: WebSocket client
        :type client: ckanext.realtime.twisted.websocket.CkanWebSocketServerProtocol
        
        '''
        log.msg("unregister client {}".format(client.peer))
            
        for client_list in self.resource_to_clients.values():
            if client in client_list:
                client_list.remove(client)
    
    def handle_message_from_client(self, json_msg, client):
        '''Handle incoming messages from WebSocket clients
        
        This method should be called through either MessageHandler
            or TestMessageHandler.
         
        :param json_msg: json string containing request body that came from client.
        :type json_msg: basestring
        :param client: WebSocket client
        :type client: ckanext.realtime.twisted.websocket.CkanWebSocketServerProtocol
        
        '''
        request = jsonpickle.decode(json_msg)
        response = None
        if request['type'] == 'datastoresubscribe':
            response = self._datastore_subscribe(request, client)
        elif request['type'] == 'datastoreunsubscribe':
            response = self._datastore_unsubscribe(request, client)
        
        if response:
            response = jsonpickle.encode(response)
            log.msg('response: ' + response)
            client.sendMessage(response)
            
    
    def handle_message_from_redis(self, json_msg):
        '''Handle incoming messages from CKAN through redis
        
        This method should be called through either MessageHandler
            or TestMessageHandler.
        
        :param json_msg: json string containing event to be sent to clients.
        :type json_msg: basestring
        
        '''
        log.msg('From Redis: ' + json_msg)
        
        event = jsonpickle.decode(json_msg)
        resource_id = event.resource_id
        
        if resource_id in self.resource_to_clients:
            response = {'event': event.__dict__}
            response['type'] = 'datastoreevent'
            
            #event_name is a class attribute so it wasn't in the __dict__
            response['event']['name'] = event.event_name
            
            for client in self.resource_to_clients[resource_id]:
                log.msg('To WSC: ' +client.peer)
                client.sendMessage(jsonpickle.encode(response))
    
    def _datastore_unsubscribe(self, request, client):
        resource_id = request['resource_id']
        result = rt.SUCCESS_MESSAGE if self._remove_subscription(resource_id, client) else rt.FAIL_MESSAGE
        
        return {'type': 'datastoreunsubscribe',
                'resource_id': resource_id,
                'result': result}
    
    def _add_subscribtion(self, resource_id, client):
        if not resource_id in self.resource_to_clients:
            self.resource_to_clients[resource_id] = []
        # the subscription has been previously registered
        if client in self.resource_to_clients[resource_id]:
            return False
        # add subscription
        self.resource_to_clients[resource_id].append(client)
        return True
    
    def _remove_subscription(self, resource_id, client):
        # must exist beforehand
        if not (resource_id in self.resource_to_clients and client in self.resource_to_clients[resource_id]):
            return False
            
        self.resource_to_clients[resource_id].remove(client)
        return True


class MessageHandler(message_handler_base):
    '''This class handles the requests from WebSocket clients and gives 
        appropriate responses.
    
    '''
    def __init__(self, api_url, apikey):
        message_handler_base.__init__(self, api_url, apikey)

    def _datastore_subscribe(self, request, client):
        
        def datastore_make_observable(resource_id, apikey):
            url = urlparse.urljoin(self.api_url, 'datastore_make_observable')
            payload = {'resource_id': resource_id}
            r = requests.post(url,
                              data=jsonpickle.encode(payload),
                              headers={'Authorization': apikey,
                                   'Content-Type': 'application/json'})
            log.msg(r.text)
            response = jsonpickle.decode(r.text)
            return response['result']['success']
            
        resource_id = request['resource_id']
        
        # ask the CKAN API if the datastore is observable
        url = urlparse.urljoin(self.api_url, 'realtime_check_observable_datastore')
        payload = {'resource_id': resource_id}
        r = requests.post(url,
                          data=jsonpickle.encode(payload),
                          headers={'Authorization': self.wss_api_key,
                                   'Content-Type': 'application/json'})
        log.msg(r.text)
        
        
        # this status code does not necessarily mean 
        # "invalid resource" (TODO: maybe should come up with something else?)
        if r.status_code == 409:
            return {'type': 'datastoresubscribe', 
                    'resource_id': request['resource_id'],
                    'result': rt.INVALID_RESOURCE_MESSAGE}
            
        # read response from the CKAN API
        response = jsonpickle.decode(r.text)
        
        # decide what to do
        is_observable = response['result']['is_observable']
        if is_observable == rt.YES_MESSAGE:
            result = rt.SUCCESS_MESSAGE if self._add_subscribtion(resource_id, client) else rt.FAIL_MESSAGE
            
            return {'type': 'datastoresubscribe', 
                    'resource_id': request['resource_id'],
                    'result': result}
            
        elif is_observable == rt.NO_MESSAGE:
            if datastore_make_observable(request['resource_id'], self.wss_api_key):
                result = rt.SUCCESS_MESSAGE
            else:
                result = rt.FAIL_MESSAGE
            
            return {'type': 'datastoresubscribe',
                    'resource_id': request['resource_id'],
                    'result': result}
            
        elif is_observable == rt.NON_DATASTORE_MESSAGE:
            return {'type': 'datastoresubscribe', 
                    'resource_id': request['resource_id'],
                    'result': rt.NON_DATASTORE_MESSAGE}


class TestMessageHandler(message_handler_base):
    '''Mock API of ClientMessageHandler for testing purposes'''
    
    def __init__(self, api_url, apikey):
        message_handler_base.__init__(self, api_url, apikey)

    def _datastore_subscribe(self, request, client):        
        resource_id = request['resource_id']
        
        if resource_id == 'observableResource':
            result = rt.SUCCESS_MESSAGE if self._add_subscribtion(resource_id, client) else rt.FAIL_MESSAGE
            return {'type': 'datastoresubscribe', 
                    'resource_id': resource_id,
                    'result': result}
            
        elif resource_id == 'nonDatastoreResource':
            return {'type': 'datastoresubscribe',
                    'resource_id': resource_id,
                    'result': rt.NON_DATASTORE_MESSAGE}
            
        else:
            return {'type': 'datastoresubscribe',
                    'resource_id': resource_id,
                    'result': rt.INVALID_RESOURCE_MESSAGE}
