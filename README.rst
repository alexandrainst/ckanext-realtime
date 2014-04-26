ckanext-realtime
================

.. image:: https://travis-ci.org/alexandrainst/ckanext-realtime.png?branch=master
	:target: https://travis-ci.org/alexandrainst/ckanext-realtime
.. image:: https://coveralls.io/repos/alexandrainst/ckanext-realtime/badge.png
	:target: https://coveralls.io/r/alexandrainst/ckanext-realtime

*ckanext-realtime* is CKAN extension which enables CKAN to serve realtime data.

**This extension is currently in the initial development stages. Please submit your ideas and PRs if you would like to contribute.**

Utilities included
------------------
#. CKAN extension which enables observable datastores
#. Datastore listener script (bin/datastore_listener)
#. WebSocket server (bin/wss)
#. JavaScript library for communication with the realtime CKAN (client/CkanRT.js)

Environment
-----------
The development work was done on an **Arch Linux** machine but it should work
with any unix like OS (travis CI builds the project on **Ubuntu**). That Said, you will need:

#. Redis Server
#. CKAN (tested on 2.2 but it should work with earlier minor releases as well).


Installation
------------

#. Install the plugin
	
	*$ python setup.py develop*
#. Install the requirements

	*$ pip install -r requirements.txt* 
#. Set ckanext-realtime specific configuration options in you ckan config (e.g. /etc/ckan/default/production.ini):
	
	*# ckanext-realtime settings*
	
	*ckan.realtime.ckan_api_url = http://localhost:5000/api/3/action/ #at what url can the Action API be reached*
	
	*ckan.realtime.apikey = <api key> 	# admin API key to be used by WebSocket server and datastore listener*
	
#. Enable the plugin in the CKAN configuration file:
	
	*ckan.plugin = ... datastore realtime # datastore plugin is a requirement for the realtime plugin*
	
#. Copy test.ini.example to test.ini and add your specific test settings


Running Python Tests
--------------------
In order to run python tests, you have to start solr server and run this command:
	
	*$ nosetests*
	
Running Jasmine Specs
---------------------
If you want to run the tests for the javascript library you have to start the websocket server:
	
	*$ python bin/wss <path_to_ckan_config> --test*

start the jasmine runner:

	*$ rake jasmine*
	
and run the tests in  your browser by navigating to *localhost:8888* in your browser. Alternatively, execute the tests directly in your shell:

	*$ rake jasmine:ci*


Copying and License
-------------------

This material is copyright (c) 2014 Alexandra Instituttet A/S.

It is open and licensed under the GNU Affero General Public License (AGPL) v3.0
whose full text may be found at:

http://www.fsf.org/licensing/licenses/agpl-3.0.html
