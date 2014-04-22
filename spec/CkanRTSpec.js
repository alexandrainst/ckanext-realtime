/*
 * These specs require the websocket server,
 * datastore listener and ckan to be running.
 */
var wsUri = "ws://127.0.0.1:9000/";
var PAUSE_BEFORE_RECONNECT = 500;
describe("CkanRT", function() {
	var rt;

	//should close the websocket after each expectation
	afterEach(function() {
		rt.websocket.close();
	});

	describe("authentication", function() {
		// the authentication process should be completed with success for the following expectations to work
		describe("when a valid ckan api key is provided", function() {
			beforeEach(function(done) {
				rt = new CkanRT(wsUri);
				rt.websocket.onopen = function(evt) {
					rt.authenticate("correctKey");
					setTimeout(function() {
						done();
					}, PAUSE_BEFORE_RECONNECT);
				};
			});

			it("should succeed", function() {
				expect(rt.authenticated).toEqual(true);
			});
		});

		describe("when an invalid ckan api key is provided", function() {
			// the authentication process should be completed with failure for the following expectations to work
			beforeEach(function(done) {
				rt = new CkanRT(wsUri);
				rt.websocket.onopen = function(evt) {
					rt.authenticate("incorrectKey");
					setTimeout(function() {
						done();
					}, PAUSE_BEFORE_RECONNECT);
				};
			});

			it("should fail", function() {
				expect(rt.authenticated).toEqual(false);
			});
		});
	});

	//TODO: this one might actually need to go through ajax instead of WebSocket
	describe("checking if datastores are observable", function() {
		// the authentication process should be completed with success for the following expectations to work
		beforeEach(function(done) {
			rt = new CkanRT(wsUri);
			rt.websocket.onopen = function(evt) {
				rt.authenticate("correctKey");
				setTimeout(function() {
					done();
				}, PAUSE_BEFORE_RECONNECT);
			};
		});

		describe("when you check observable datastores", function() {
			it("should give possitive answer", function() {
				expect(true).toEqual(false);
			});
		});

		describe("when you check non-observable datastores", function() {
			it("should give negative answer", function() {
				expect(true).toEqual(false);
			});
		});

		describe("when you check non-datastore resources", function() {
			it("should indicate error", function() {
				expect(true).toEqual(false);
			});
		});

		describe("when you check invalid resources", function() {
			it("should indicate error", function() {
				expect(true).toEqual(false);
			});
		});
	});

	//TODO: this one might actually need to go through ajax instead of WebSocket
	describe("making resources observable", function() {
		// the authentication process should be completed with success for the following expectations to work
		beforeEach(function(done) {
			rt = new CkanRT(wsUri);
			rt.websocket.onopen = function(evt) {
				rt.authenticate("correctKey");
				setTimeout(function() {
					done();
				}, PAUSE_BEFORE_RECONNECT);
			};
		});
		describe("when a resource is a non-observable datastore", function() {
			it("should succeed", function() {
				expect(true).toEqual(false);
			});
		});

		describe("when a resource is an observable datastore", function() {
			it("should indicate failure", function() {
				expect(true).toEqual(false);
			});
		});

		describe("when a resource isn't a datastore", function() {
			it("should indicate failure", function() {
				expect(true).toEqual(false);
			});
		});
	});

	describe("subscribing/unsubscribing from observable datastores", function() {
		// the authentication process should be completed with success for the following expectations to work
		beforeEach(function(done) {
			rt = new CkanRT(wsUri);
			rt.websocket.onopen = function(evt) {
				rt.authenticate("correctKey");
				setTimeout(function() {
					done();
				}, PAUSE_BEFORE_RECONNECT);
			};
		});

		describe("when you subscribe/unsubscribe from observable datastores", function() {
			it("should succeed", function(done) {
				var resource = "observableResource";
				var expectedResult = "SUCCESS";
				rt.onDatastoreSubscribeResult = function(resourceId, status) {
					expect(resourceId).toEqual(resource);
					expect(status).toEqual(expectedResult);
					rt.onDatastoreUnsubscribeResult = function(resourceId, status) {
						expect(resourceId).toEqual(resource);
						expect(status).toEqual(expectedResult);
						done();
					};
					rt.datastoreUnsubscribe(resource);
				};
				rt.datastoreSubscribe(resource);
			});
		});

		describe("when you subscribe/unsubscribe from non-observable datastores", function() {
			it("should fail", function(done) {
				var resource = "nonObservableResource";
				var expectedResult = "FAIL";
				rt.onDatastoreSubscribeResult = function(resourceId, status) {
					expect(resourceId).toEqual(resource);
					expect(status).toEqual(expectedResult);
					rt.onDatastoreUnsubscribeResult = function(resourceId, status) {
						expect(resourceId).toEqual(resource);
						expect(status).toEqual(expectedResult);
						done();
					};
					rt.datastoreUnsubscribe(resource);
				};
				rt.datastoreSubscribe(resource);
			});
		});

		describe("when you subscribe/unsubscribe from non-datastore resources", function() {
			it("should fail with error", function(done) {
				var resource = "nonDatastoreResource";
				var expectedResult = "NOT-A-DATASTORE";
				rt.onDatastoreSubscribeResult = function(resourceId, status) {
					expect(resourceId).toEqual(resource);
					expect(status).toEqual(expectedResult);
					rt.onDatastoreUnsubscribeResult = function(resourceId, status) {
						expect(resourceId).toEqual(resource);
						expect(status).toEqual(expectedResult);
						done();
					};
					rt.datastoreUnsubscribe(resource);
				};
				rt.datastoreSubscribe(resource);
			});
		});

		describe("when you subscribe/subscribe from invalid resources", function() {
			it("should fail with error", function(done) {
				var resource = "invalidResource";
				var expectedResult = "INVALID-RESOURCE";
				rt.onDatastoreSubscribeResult = function(resourceId, status) {
					expect(resourceId).toEqual(resource);
					expect(status).toEqual(expectedResult);
					rt.onDatastoreUnsubscribeResult = function(resourceId, status) {
						expect(resourceId).toEqual(resource);
						expect(status).toEqual(expectedResult);
						done();
					};
					rt.datastoreUnsubscribe(resource);
				};
				rt.datastoreSubscribe(resource);
			});
		});

		afterEach(function() {
			rt.websocket.close();
		});
	});
});
