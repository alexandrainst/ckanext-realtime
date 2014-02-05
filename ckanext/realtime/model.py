from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ObservableDatastoreMetadata(Base):
    ''' Represents metadata for Observable Datastore '''
    __tablename__ = '_realtime_metadata'
    
    uuid = Column(String(36), primary_key=True)
    
    @classmethod
    def get(cls, read_session, reference):
        res = read_session.query(cls).filter_by(uuid=reference).first()
        return res
    
    @classmethod
    def initiate_table(cls, write_connection, override_if_exists=False):
        ''' Creates table for ObservableDatastoreMetadata model
        
        Parameters:
        -----------
        :param write_connection:
        :param override_if_exists: should the table be dropped if it exists
        :type override_if_exists: bool
        '''
        if override_if_exists:
            Base.metadata.drop_all(write_connection, [cls.__table__])
            
        Base.metadata.create_all(write_connection, [cls.__table__])
    
    def __repr__(self):
        return '{0}(uuid={1}) '.format(self.__class__, self.uuid)


