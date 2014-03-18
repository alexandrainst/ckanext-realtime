import logging

import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import exists

from ckanext.realtime.exc import RealtimeError

log = logging.getLogger(__name__)
_engines = {}
    
    
def add_datastore_notifier_trigger(write_url, resource_id):
    sql = '''
        DROP TRIGGER IF EXISTS "{res}_notifier" ON "{res}" RESTRICT;
    
        CREATE TRIGGER "{res}_notifier"
        BEFORE INSERT OR UPDATE OR DELETE ON  "{res}"
        FOR EACH ROW
        EXECUTE PROCEDURE datastore_notifier();
    '''.format(res=resource_id)
    
    try:
        connection = get_engine(write_url).connect()
        connection.execute(sql)
    finally:
        connection.close()


def create_datastore_notifier_trigger_function(write_url):
    '''Create a function for datastore tables used to notify about changes.
    
    :param write_url: sqlalchemy url with write access to datastore database.
    :type write_url: string
    
    '''
    sql = """
        CREATE OR REPLACE FUNCTION "public"."datastore_notifier" () RETURNS trigger AS 'BEGIN
            EXECUTE ''NOTIFY ckanextrealtime, '''''' || TG_OP || '' '' || TG_TABLE_NAME || '''''';'';
            RETURN NULL;
        END' LANGUAGE "plpgsql" COST 100
        VOLATILE
        CALLED ON NULL INPUT
        SECURITY DEFINER;
    """
    
    try:
        connection = get_engine(write_url).connect()
        connection.execute(sql)
    finally:
        connection.close()


def get_engine(connection_url):
    '''Get either read or write engine.'''
    engine = _engines.get(connection_url)

    if not engine:
        engine = sqlalchemy.create_engine(connection_url)
        _engines[connection_url] = engine
    return engine


class SessionFactory(object):
    '''Factory class which makes sqlalchemy orm sessions'''
    _configured = False
    
    _configuration_error_msg = 'SessionFactory has not been configured'
    
    _ReadSession = sessionmaker()
    _WriteSession = sessionmaker()
    
    @classmethod
    def configure(cls, read_connection_url, write_connection_url):
        '''Configure SessionFactory
        
        :param read_connection_url: sqlalchemy url of connection used for 
            reading
        :type read_connection_url: string
        :param write_connection_url: sqlalchemy url of connection used for 
            writing
        :type write_connection_url: string 
        
        '''
        cls._configured = True
        
        cls._read_engine = get_engine(read_connection_url)
        cls._ReadSession.configure(bind=cls._read_engine)
            
        cls._write_engine = get_engine(write_connection_url)
        cls._WriteSession.configure(bind=cls._write_engine)
    
    @classmethod
    def get_read_session(cls):
        '''Makes an sql alchemy orm session for reading.
        You have to configure the SessionFactory class before calling this
        method.
        
        :return: orm session associated with read engine
        :rtype: sqlalchemy.orm.session.Session
        
        '''
        if not cls._configured:
            raise RealtimeError(cls._configuration_error_msg)
        return cls._ReadSession()
          
    @classmethod
    def get_write_session(cls):
        '''Makes an sql alchemy orm session for writing.
        You have to configure the SessionFactory class before calling this
        method.
        
        :return: orm session associated with write engine
        :rtype: sqlalchemy.orm.session.Session
        
        '''
        if not cls._configured:
            raise RealtimeError(cls._configuration_error_msg)
        return cls._WriteSession()
    
    @classmethod
    def get_read_engine(cls):
        '''Returns sqlalchemy engine for reading'''
        if not cls._configured:
            raise RealtimeError(cls._configuration_error_msg)
        return cls._read_engine
    
    @classmethod
    def get_write_engine(cls):
        '''Returns sqlalchemy engine for writing'''
        if not cls._configured:
            raise RealtimeError(cls._configuration_error_msg)
        return cls._write_engine

