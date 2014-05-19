/*
 * These specs require the websocket server to be running in test mode:
 * - python bin/ckan_wss <path_to_ckan_config> --test
 */
var wsUri = "ws://127.0.0.1:9000/";

describe("CkanRT", function() {
	var rt;

	describe("subscribing/unsubscribing from observable datastores", function() {
		//should initiate WebSocket connection before each expectation
		beforeEach(function(done) {
			rt = new CkanRT(wsUri);
			rt.websocket.onopen = function() {
				done();
			};
		});

		//should close the WebSocket connection after each expectation
		afterEach(function() {
			rt.websocket.close();
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
	});
});
