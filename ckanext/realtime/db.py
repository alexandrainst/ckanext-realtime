import logging

import sqlalchemy

log = logging.getLogger(__name__)

# should set in plugin.py
WRITE_URL = ''
READ_URL = ''
    
    
def add_datastore_notifier_trigger(resource_id):
    sql = '''
        DROP TRIGGER IF EXISTS "{res}_notifier" ON "{res}" RESTRICT;
    
        CREATE TRIGGER "{res}_notifier"
        AFTER INSERT OR UPDATE OR DELETE ON "{res}"
        FOR EACH ROW
        EXECUTE PROCEDURE datastore_notifier();
    '''.format(res=resource_id)
    
    engine = sqlalchemy.create_engine(WRITE_URL)
    engine.execute(sql)


def create_datastore_notifier_trigger_function():
    '''Create a function for datastore tables used to notify about changes.
    
    :param write_url: sqlalchemy url with write access to datastore database.
    :type write_url: string
    
    '''
    global write_url
    
    sql = """
        CREATE OR REPLACE FUNCTION "public"."datastore_notifier" () RETURNS trigger AS 'BEGIN
            EXECUTE ''NOTIFY ckanextrealtime, '''''' || TG_OP || '' '' || TG_TABLE_NAME || '''''';'';
            RETURN NEW;
        END' LANGUAGE "plpgsql" COST 100
        VOLATILE
        CALLED ON NULL INPUT
        SECURITY DEFINER;
    """
    
    engine = sqlalchemy.create_engine(WRITE_URL)
    engine.execute(sql)
