import logging
import pylons

import sqlalchemy

log = logging.getLogger(__name__)
    
    
def add_datastore_notifier_trigger(resource_id):
    '''This trigger sends datastore events to bin/datastore_listener script'''
    
    sql = '''
        DROP TRIGGER IF EXISTS "{res}_notifier" ON "{res}" RESTRICT;
    
        CREATE TRIGGER "{res}_notifier"
        AFTER INSERT OR UPDATE OR DELETE ON "{res}"
        FOR EACH ROW
        EXECUTE PROCEDURE datastore_notifier();
    '''.format(res=resource_id)
    
    engine = sqlalchemy.create_engine(pylons.config['ckan.datastore.write_url'])
    engine.execute(sql)


def create_datastore_notifier_trigger_function():
    '''Create a function for datastore tables used to notify about changes.'''
    
    sql = """
        CREATE OR REPLACE FUNCTION "public"."datastore_notifier" () RETURNS trigger AS 'BEGIN
            EXECUTE ''NOTIFY ckanextrealtime, '''''' || TG_OP || '' '' || TG_TABLE_NAME || '''''';'';
            RETURN NEW;
        END' LANGUAGE "plpgsql" COST 100
        VOLATILE
        CALLED ON NULL INPUT
        SECURITY DEFINER;
    """
    
    engine = sqlalchemy.create_engine(pylons.config['ckan.datastore.write_url'])
    engine.execute(sql)
    
    
def notifier_trigger_function_exists(resource_id):
    sql = sqlalchemy.text('SELECT * FROM pg_trigger WHERE tgname = :tg;')
    
    engine = sqlalchemy.create_engine(pylons.config['ckan.datastore.write_url'])
    results = engine.execute(sql, tg='{}_notifier'.format(resource_id))
    return results.rowcount == 1
