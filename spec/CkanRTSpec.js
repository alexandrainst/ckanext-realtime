/*
 * These specs require the websocket server,
 * datastore listener and ckan to be running.
 */
var wsUri = "ws://127.0.0.1:9000/";
describe("CkanRT", function() {

	describe("successful authentication", function() {
		var rt;
		beforeEach(function(done) {
			rt = new CkanRT(wsUri);
			rt.websocket.onopen = function(evt) {
				rt.authenticate("correctKey");
				setTimeout(function() {
					done();
				}, 1000);
			};
		});

		it("should succeed within 1 second", function() {
			expect(rt.authenticated).toEqual(true);
		});

		afterEach(function() {
			rt.websocket.close();
		});
	});

	describe("unsuccessful authentication", function() {
		var rt;
		beforeEach(function(done) {
			rt = new CkanRT(wsUri);
			rt.websocket.onopen = function(evt) {
				rt.authenticate("incorrectKey");
				setTimeout(function() {
					done();
				}, 1000);
			};
		});

		it("should fail within 1 second", function() {
			expect(rt.authenticated).toEqual(false);
		});

		afterEach(function() {
			rt.websocket.close();
		});
	});

});
