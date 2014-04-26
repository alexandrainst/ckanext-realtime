function CkanRT(websocketUrl) {
	this.websocketUrl = websocketUrl;
	this.authenticated = false;
	this.init();
}

// START BLOCK - these methods should be overriden by the api user
CkanRT.prototype.onAuth = function() {
	//empty
};

CkanRT.prototype.onDatastoreSubscribeResult = function(resourceId, status) {

};

CkanRT.prototype.onDatastoreUnsubscribedResult = function(resourceId, status) {

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

CkanRT.prototype.isDatastoreObservable = function(resourceId) {
	//TODO: implement
};

CkanRT.prototype.datastoreMakeObservable = function(resourceId) {
	//TODO: implement
};

CkanRT.prototype.authenticate = function(apiKey) {
	var packet = {
		type : 'auth',
		apikey_to_check : apiKey
	};
	this.websocket.send(JSON.stringify(packet));
};

function messageReceived(message, rt) {
	console.log(message);
	var payload = JSON.parse(message.data);
	switch (payload.type) {
		case 'auth':
			if (payload.result) {
				rt.authenticated = true;
				rt.onAuth();
				console.log('successful auth');
			} else {
				console.log('unsuccessful auth');
			}
			break;
		case 'datastoresubscribe':
			rt.onDatastoreSubscribeResult(payload.resource_id, payload.result);
			break;
		case 'datastoreunsubscribe':
			rt.onDatastoreUnsubscribeResult(payload.resource_id, payload.result);
			break;
		default:
			console.log('unrecognized payload');
	}
}

// CkanRT.prototype.emitControlEvent = function(event) {
//
// };

