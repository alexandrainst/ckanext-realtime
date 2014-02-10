import logging

import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import exists

from ckanext.realtime.exc import RealtimeError
from ckanext.realtime.model import ObservableDatastoreMetadata

log = logging.getLogger(__name__)

_engines = {}

def mark_as_observable(resource_id):
    '''
    Marks datastore as observable by inserting a row into _realtime_metadata
        table.
        
    :param resource_id: resource id that identifies datastore.
    :type resource_id: uuid
    :returns: success indicator
    :rtype: bool
    '''
    if is_observable(resource_id):
        return True
    
    s = SessionFactory.get_write_session()
    meta = ObservableDatastoreMetadata(uuid=resource_id)
    s.add(meta)
    
    try:
        s.commit()
    except SQLAlchemyError, e:
        log.error(str(e))
        return False
    return True

def is_observable(resource_id):
    '''
    Returns true if the datastore under the specified resource is observable.
    
    :param resource_id: resource id that identifies datastore.
    :type resource_id: str
    :returns: success indicator
    :rtype: bool
    '''
    s = SessionFactory.get_read_session()
    return (s.query(exists()
            .where(ObservableDatastoreMetadata.uuid == resource_id)).scalar())

def create_metadata_table(write_url):
    ''' 
    ckanext-realtime has some additional metadata on top of the metadata
    in ckanext-datastore.
    '''     
    try:
        connection = _get_engine(write_url).connect()
        ObservableDatastoreMetadata.initiate_table(connection)
    finally:
        connection.close() 
    
    
def _get_engine(connection_url):
    '''Get either read or write engine.'''
    engine = _engines.get(connection_url)

    if not engine:
        engine = sqlalchemy.create_engine(connection_url)
        _engines[connection_url] = engine
    return engine

class SessionFactory(object):
    ''' Factory class which makes sqlalchemy orm sessions '''
    _configured = False
    
    _configuration_error_msg = 'SessionFactory has not been configured'
    
    _ReadSession = sessionmaker()
    _WriteSession = sessionmaker()
    
    @classmethod
    def configure(cls, read_connection_url, write_connection_url):
        ''' Configure SessionFactory
        
        :param read_connection_url: sqlalchemy url of connection used for 
            reading
        :type read_connection_url: string
        :param write_connection_url: sqlalchemy url of connection used for 
            writing
        :type write_connection_url: string 
        '''
        cls._configured = True
        
        read_engine = _get_engine(read_connection_url)
        cls._ReadSession.configure(bind=read_engine)
            
        write_engine = _get_engine(write_connection_url)
        cls._WriteSession.configure(bind=write_engine)
    
    @classmethod
    def get_read_session(cls):
        ''' Makes an sql alchemy orm session for reading.
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
        ''' Makes an sql alchemy orm session for writing.
        You have to configure the SessionFactory class before calling this
        method.
        
        :return: orm session associated with write engine
        :rtype: sqlalchemy.orm.session.Session
        '''
        if not cls._configured:
            raise RealtimeError(cls._configuration_error_msg)
        return cls._WriteSession()