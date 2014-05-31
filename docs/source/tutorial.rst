Realtime apps with CKAN (Tutorial) 
==================================

Intro
-----

`ckanext-realtime <https://github.com/alexandrainst/ckanext-realtime>`_ is the latest contributions to Free Software from Gatesense team. It is an extension for CKAN open data platform which enables app developers to make realtime applications with CKAN. More specifically, you can subscribe to resources (datastores) and thus monitor their changes in realtime. gatesense.com is a realtime-enabled CKAN portal, among other things. This means that you can build realtime apps with datasets found at http://gatesense.com/ckan/dataset .


Requirements
------------
To complete this tutorial, you will need a CKAN data portal with ckanext-realtime installed and a bit of JavaScript, jQuery and HTML knowledge. CKAN Action API knowledge is not necessary as it is relatively straightforward. You may either setup your own CKAN instance or use `gatesense.com <http://gatesense.com>`_ because it already has ckanext-realtime installed on it.

Tutorial
--------

For this tutorial we will use a dummy dataset - `ckanext-realtime showcase <http://gatesense.com/ckan/dataset/ckanext-realtime-showcase>`_. Alternatively, you can choose to use a dataset that contains real data like Realtime traffic data on `gatesense <http://gatesense.com/ckan/datasets>`_.

Our client application will reload resource presentation in realtime, every time some new data comes in (much like this `one <http://gatesense.com/realtime/examples/ex2/>`_ ).

In order to achieve realtime, ckanext-realtime uses WebSocket protocol. The WebSocket server is running on ws://gatesense.com:9998/ .

Step 1 - download CkanRT.js library
-----------------------------------
CkanRT.js is a simple abstraction on top of Javascript WebSocket client. You can find it on `github <https://github.com/alexandrainst/ckanext-realtime/blob/master/client/CkanRT.js>`_. Download it and place it in your app directory.

Step 2 - basic structure
------------------------
We will start with an app with CkanRT and jQuery included which simply renders our resource data in a table:


.. code-block:: html

    <!DOCTYPE html>
    
    <meta charset="utf-8" />
    
    <title>Realtime Apps with CKAN - Tutorial</title>
    
    <script src="http://code.jquery.com/jquery-1.11.0.min.js"></script>
    <script src="CkanRT.js"></script>
    
    <script language="javascript" type="text/javascript">
    	var datastore = '07324b49-37d8-4c43-8077-df0f8a430f79';
    	var actionApiRoot = 'http://gatesense.com/ckan/api/3/action/';
    	var apikey = '<your api key>';
    
    	$(document).ready(function() {
    		init();
    	});
    
    	function init() {
                reload();
    	}
    
            //get resource data via CKAN Action API and draw a table out of it
            function reload() {
    		$.ajax({
    		    url : actionApiRoot + 'datastore_search?resource_id=' + datastore + '&sort=_id',
    		    type : 'GET',
    		    success : function(data) {
    
                            // iterate through results and construct a table out of them
    		        var table = '<table border="1" style="border-collapse: collapse"><tr><th>_id</th><th>message</th><th>timestamp</th></tr>';
    		        for (i in data.result.records) {
    		            var current = data.result.records[i];
    		            table += '<tr><td>' + current._id + '</td><td>' + current.message + '</td><td>' + current.timestamp + '</td></tr>';
    		        }
    		        table += '</table>';
    		        
    		        $('#content').html(table);
                            writeLog('Resource reloaded.');
    		    }
    		});
            }
    
    
            // outputs messages to log on screen
    	function writeLog(message, error) {
                var color = 'blue';
                if (error) {
                    color = 'red';
                }
    
                var messageHtml = '<span style="color: ' + color + ';">' + message + '</span><br>';
    	    $('#log').append(messageHtml);
    	}
    
    </script>
    <h2>Realtime Apps with CKAN - Tutorial</h2>
    
    <div id="content"></div>
    <br>
    <div id="log"></div>

If view the page now, you should be able to see some data rendered in table.

Step 3 - insert data
--------------------
Next step, implement a function to insert data. The function:

.. code-block:: javascript

        //insert a new tuple into the sample datastore
	function insertToDatastore(msg, datastore) {
		var now = new Date();

                //construct the payload
		var data = {
			resource_id : datastore,
			records : [{
				message : msg,
				timestamp : now.toISOString()
			}],
		};

		writeLog('Inserting into ' + datastore + '...');

		jQuery.ajax({
			url : actionApiRoot + 'datastore_create',
			type : 'POST',

                        // You must authenticate with apikey when inserting
			beforeSend : function(request) {
				request.setRequestHeader("Authorization", apikey);
			},

			data : JSON.stringify(data),
			dataType : 'application/json',
		});
	}

Now add some html for inputing text (just above the ouput):

.. code-block:: html

        <div id="input">
        	<label>Insert Into Datastore</label>
        	<br>
        	<input type="text" name="message" id="message">
        	<input type="button" name="insert" value="Insert">
        </div>

And hook up the button with some javascript in the init method:

.. code-block:: javascript

        $("input[name='insert']").click(function() {
        	var msg = jQuery("#message").val();
        	insertToDatastore(msg, datastoreResource);
        });

Step 4 - connect to notification server and subscribe to resource notifications
-------------------------------------------------------------------------------
We've got an app which can insert data into datastore and display its data.
Let's connect to our realtime server and subscribe to resource notifications (in the init method):

.. code-block:: javascript

            //connect to notification server
	    var rt = new CkanRT('ws://gatesense.com:9998/');

	    // define CkanRT callbacks

            //called when notification server reports back with subscribing status
	    rt.onDatastoreSubscribeResult = function(resourceId, status) {
	    	writeLog('Subscribe to ' + resourceId + '. Status: ' + status);
	    };

            //called when notification server reports back with unsubscribing status
	    rt.onDatastoreUnsubscribeResult = function(resourceId, status) {
	    	writeLog('Unsubscribe from ' + resourceId + '. Status: ' + status);
	    };

            //new event on one of your subscribtions
	    rt.onDatastoreEvent = function(event) {
	    	writeLog('New event: ' + JSON.stringify(event));
	    };

	    //end of CkanRT specific callbacks

	    //some WebSocket callbacks

            //subscribe to datastoreResource when WebSocket connection opens
	    rt.websocket.onopen = function(evt) {
	    	writeLog("Connection to notification server opened.");
	    	rt.datastoreSubscribe(datastoreResource);
	    };

            //connection closed
	    rt.websocket.onclose = function(evt) {
	    	writeLog("Disconnected from notification server");
	    };

            //something's wrong...
	    rt.websocket.onerror = function(evt) {
	    	writeLog('ERROR:' + evt.data, true);
	    };
            //end of WebSocket callbacks


Step 5 - reload the table in realtime
-------------------------------------
One last thing- let's reload the table when we get a notification because I'm really tired of pressing F5 :)

.. code-block:: javascript

    rt.onDatastoreEvent = function(event) {
    	writeLog('New event: ' + JSON.stringify(event));
        reload(datastoreResource);
    };


Step 6 - We're done!
--------------------
You can find the code for this app `here <http://gatesense.com/snippets/realtime-tutorial.zip>`_. You call also see the app `running <http://gatesense.com/realtime-tutorial>`_


What's next?
------------
OK, so this app isn't very nice- can you come up with something better? Register at `gatesense.com <http://gatesense.com>`_, get your apikey and start hacking . I look forward to see what you build :)
