'''
Listen for events from datastore tables using PostgreSQL LISTEN/NOTIFY.
'''

import argparse
import json
import psycopg2.extensions
import requests
import select
import ConfigParser

import ckanext.realtime.db as db

def call_ckan_api(notify, ckan_api_url, api_key):
    '''Parses NOTIFY packages and forwards the info to ckan api.
    
    :param notify: NOTIFY package issued from datastore
    :param ckan_api_url: action api endpoint
        (E.g. 'http://localhost:5000/api/3/action/')
    
    :param api_key: ckan api key for this script, used to call
        'realtime_broadcast_events' action
        
    '''
    url = ckan_api_url + 'realtime_broadcast_events'
    auth_header = {'Authorization': api_key,
                   'content-type': 'application/json'}
    
    print type(notify)
    tokens = notify.payload.split()
    try:
        op = tokens[0]
        resource_id = tokens[1]
    except IndexError, e:
        print e
        return
    except Exception, e:
        print e
        return
    
    if op == 'INSERT':
        event_type = 'datastore_insert'
    elif op == 'UPDATE':
        event_type = 'datastore_update'
    elif op == 'DELETE':
        event_type = 'datastore_delete'
    else:
        print 'unrecognized operation!'
        return
    
    payload = {'event_type': event_type, 'resource_id': resource_id}
    r = requests.post(url, data=json.dumps(payload), headers=auth_header)
    print r.text


def make_connection(sqlalchemy_url):
    engine = db.get_engine(sqlalchemy_url)
    base_conn = engine.connect()
    sub_conn = base_conn.connection
    psycopg_conn = sub_conn.connection
    return psycopg_conn


def main(config):
    datastore_url = config.get('app:main', 'ckan.datastore.read_url')
    api_key = config.get('app:main', 'ckan.realtime.datastore_listener_api_key')
    ckan_api_url = config.get('app:main', 'ckan.realtime.ckan_api_url')

    conn = make_connection(datastore_url)
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    curs = conn.cursor()
    curs.execute("LISTEN ckanextrealtime;")

    print "Waiting for notifications on channel 'chanextrealtime'"
    while 1:
        if select.select([conn],[],[],5) == ([],[],[]):  #5 second timeout
            print "."
        else:
            conn.poll()
            while conn.notifies:
                notify = conn.notifies.pop()
                print "Got NOTIFY:", notify.pid, notify.channel, notify.payload
                call_ckan_api(notify, ckan_api_url, api_key)
                

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Listen for events from PostgreSQL datastores with LISTEN/NOTIFY.')
    parser.add_argument("config")
    args = parser.parse_args()
    
    config = ConfigParser.RawConfigParser()
    config.read(args.config)
    
    main(config)
