function CkanRT(websocketUrl) {
	this.websocketUrl = websocketUrl;
	this.activeDatastores = new Array();
	this.authenticated = false;
	this.init();
}

// START BLOCK - these methods should be overriden by the api user
CkanRT.prototype.onauth = function() {
	//empty
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
	//TODO: implement
};

CkanRT.prototype.datastoreUnsubscribe = function(resourceId) {
	//TODO: implement
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
		apikey : apiKey
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
				rt.onauth();
				console.log('successful auth');
			} else {
				console.log('unsuccessful auth');
			}
			break;
		default:
			console.log('unrecognized payload');
	}
}

// CkanRT.prototype.emitControlEvent = function(event) {
//
// };

