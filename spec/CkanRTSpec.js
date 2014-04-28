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
		describe("when a valid ckan api key is provided", function() {
			it("should succeed", function() {
				rt = new CkanRT(wsUri);
				rt.websocket.onopen = function(evt) {
					rt.onAuth = function(status) {
						expect(status).toEqual('SUCCESS');
					};
					rt.authenticate("correctKey");
				};
			});
		});

		describe("when an invalid ckan api key is provided", function() {
			it("should fail", function() {
				rt = new CkanRT(wsUri);
				rt.websocket.onopen = function(evt) {
					rt.onAuth = function(status) {
						expect(status).toEqual('FAIL');
					};
					rt.authenticate("incorrectKey");
				};
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

		describe("when you subscribe to the same datastore repeatedly", function() {
			it("should fail", function(done) {
				var resource = "observableResource";
				var expectedResult = "SUCCESS";
				rt.onDatastoreSubscribeResult = function(resourceId, status) {
					expect(resourceId).toEqual(resource);
					expect(status).toEqual(expectedResult);

					expectedResult = "FAIL";
					rt.onDatastoreSubscribeResult = function(resourceId, status) {
						expect(resourceId).toEqual(resource);
						expect(status).toEqual(expectedResult);
						done();
					};
					rt.datastoreSubscribe(resource);
				};
				rt.datastoreSubscribe(resource);

			});
		});

		describe("when you unsubscribe from previously not subscribed datastore", function() {
			it("should fail", function(done) {
				var resource = "observableResource";
				var expectedResult = "FAIL";
				rt.onDatastoreUnsubscribeResult = function(resourceId, status) {
					expect(resourceId).toEqual(resource);
					expect(status).toEqual(expectedResult);
					done();
				};
				rt.datastoreUnsubscribe(resource);
			});
		});

		describe("when you subscribe to non-observable datastores", function() {
			it("should fail", function(done) {
				var resource = "nonObservableResource";
				var expectedResult = "FAIL";
				rt.onDatastoreSubscribeResult = function(resourceId, status) {
					expect(resourceId).toEqual(resource);
					expect(status).toEqual(expectedResult);
					done();
				};
				rt.datastoreSubscribe(resource);
			});
		});

		describe("when you subscribe to non-datastore resources", function() {
			it("should fail with error", function(done) {
				var resource = "nonDatastoreResource";
				var expectedResult = "NOT-A-DATASTORE";
				rt.onDatastoreSubscribeResult = function(resourceId, status) {
					expect(resourceId).toEqual(resource);
					expect(status).toEqual(expectedResult);
					done();
				};
				rt.datastoreSubscribe(resource);
			});
		});

		describe("when you subscribe to invalid resources", function() {
			it("should fail with error", function(done) {
				var resource = "invalidResource";
				var expectedResult = "INVALID-RESOURCE";
				rt.onDatastoreSubscribeResult = function(resourceId, status) {
					expect(resourceId).toEqual(resource);
					expect(status).toEqual(expectedResult);
					done();
				};
				rt.datastoreSubscribe(resource);
			});
		});

		afterEach(function() {
			rt.websocket.close();
		});
	});
});
