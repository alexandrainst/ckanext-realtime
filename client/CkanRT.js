function CkanRT(websocketUrl) {
	this.websocketUrl = websocketUrl;
	this.init();
}

// START BLOCK - these methods should be overriden by the API user
CkanRT.prototype.onAuth = function(status) {

};

CkanRT.prototype.onDatastoreSubscribeResult = function(resourceId, status) {

};

CkanRT.prototype.onDatastoreUnsubscribedResult = function(resourceId, status) {

};

CkanRT.prototype.onDatastoreEvent = function(event) {

};

// END BLOCK

CkanRT.prototype.init = function() {
	this.websocket = new WebSocket(this.websocketUrl);

	var rt = this;
	this.websocket.onmessage = function(msg) {
		messageReceived(msg, rt);
	};
};

CkanRT.prototype.datastoreSubscribe = function(resourceId) {
	var packet = {
		type : 'datastoresubscribe',
		resource_id : resourceId,
	};
	this.websocket.send(JSON.stringify(packet));
};

CkanRT.prototype.datastoreUnsubscribe = function(resourceId) {
	var packet = {
		type : 'datastoreunsubscribe',
		resource_id : resourceId,
	};
	this.websocket.send(JSON.stringify(packet));
};

CkanRT.prototype.authenticate = function(apiKey) {
	var packet = {
		type : 'auth',
		apikey_to_check : apiKey
	};
	this.websocket.send(JSON.stringify(packet));
};

function messageReceived(message, rt) {
	var payload = JSON.parse(message.data);
	switch (payload.type) {
		case 'auth':
			rt.onAuth(payload.result);
			break;
		case 'datastoresubscribe':
			rt.onDatastoreSubscribeResult(payload.resource_id, payload.result);
			break;
		case 'datastoreunsubscribe':
			rt.onDatastoreUnsubscribeResult(payload.resource_id, payload.result);
			break;
		case 'datastoreevent':
			rt.onDatastoreEvent(payload.event);
			break;
		default:
			console.log('unrecognized payload');
	}
}
