import sqlalchemy as db
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


hostname = '172.17.0.1'


#engine = create_engine(f'mysql+mysqlconnector://sat:123@{hostname}:3306/satellites', echo=True)
#try:
#    connection = engine.connect()
#    print('Connected via mysqlconnector')
#except:
#    print('Could not connect with mysqlconnector')


engine = db.create_engine(f'mysql+pymysql://sat:123@{hostname}:3306/satellites', echo=True)
try:
    connection = engine.connect()
    print('Connected via pymysql')
except:
    print('Could not connect with pymysql')


Base = declarative_base()


class Satellite(Base):
    __tablename__ = 'satellites'

    id = db.Column(db.String(length=10), primary_key=True)
    name = db.Column(db.String(length=255))
    metric = db.Column(db.String(length=255))

    def __repr__(self):
        return f'<Satellite {self.id}>'


class FileImport(Base):
    __tablename__ = 'file_imports'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(length=255))
    start_dt = db.Column(db.DateTime)
    end_dt = db.Column(db.DateTime)

    def __repr__(self):
        return f'<FileImport {self.id}>'


class SatelliteData(Base):
    __tablename__ = 'satellite_data'
    
    id = db.Column(db.Integer, primary_key=True)
    file_import_id = db.Column(db.Integer, db.ForeignKey('file_imports.id'))
    file_import = relationship('FileImport')
    satellite_id = db.Column(db.String(length=10), db.ForeignKey('satellites.id'))
    satellite = relationship('Satellite')
    measurement_dt = db.Column(db.DateTime)
    ionosphere = db.Column(db.Float)
    ndvi = db.Column(db.Float)
    radiation = db.Column(db.Float)
    measurement = db.Column(db.String(length=255))

    def __repr__(self):
        return f'<SatelliteData {self.id}>'


Base.metadata.create_all(engine)


Session = db.orm.sessionmaker()
Session.configure(bind=engine)
session = Session()

# add satellites
sat1 = Satellite(id='30J14', name='SPOT7', metric='Earth Altitude')
sat2 = Satellite(id='8J14', name='SKYSAT2', metric='Vegetation Classification')
sat3 = Satellite(id='13A14', name='WORLDVIEW3', metric='Sea Salinity')
sat4 = Satellite(id='6N14', name='ASNARO1', metric='Sea Salinity')
session.add(sat1)
session.add(sat2)
session.add(sat3)
session.add(sat4)
session.commit()

# add a user
#user = User(name='Brad', fullname='Brad Allen Luczywo', nickname='Cheezer')
#session.add(user)
#session.commit()

# query the user
#our_user = session.query(User).filter_by(name='Brad').first()
#print('\nOur User:')
#print(our_user)
#print(f'Nickname: {our_user.nickname}')
