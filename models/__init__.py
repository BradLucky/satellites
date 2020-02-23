"""Provides access to the database via SQLAlchemy and defines the data models."""
import csv
import os
from datetime import datetime

import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()
engine = None


def init_db(app):
    """Initialize the database session for accessing it.

    Attempt to get the URI from the Docker container, falling
    back to the OS environment variable if that fails.
    """
    global engine
    global session

    database_uri = app.config.get(
        'MYSQL_DATABASE_URI',
        os.environ.get('MYSQL_DATABASE_URI')
    )

    try:
        engine = db.create_engine(database_uri)
    except TypeError:
        raise AttributeError('DB engine could not be initialized')

    Session = db.orm.sessionmaker()
    Session.configure(bind=engine)
    session = Session()

    return session


class Satellite(Base):
    __tablename__ = 'satellites'

    id = db.Column(db.String(length=10), primary_key=True)
    name = db.Column(db.String(length=255))
    metric = db.Column(db.String(length=255))

    def __repr__(self):
        return f'<Satellite ({self.name})>'


class FileImport(Base):
    __tablename__ = 'file_imports'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(length=255))
    start_dt = db.Column(db.DateTime)
    end_dt = db.Column(db.DateTime)

    def __repr__(self):
        return f'<FileImport ({self.id})>'


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
        return f'<SatelliteData ({self.id})>'


def add_satellites(session_override=None):
    """Initialize the database with the 4 original satellites.

    Simply loop through the dictionary of defined satellites
    and create a Satellite object as a database model object.
    After a commit at the end, these are ready to use.
    """
    if session_override:
        session = session_override

    def_satellites = [
        {'id': '30J14', 'name': 'SPOT7', 'metric': 'Earth Altitude'},
        {'id': '8J14', 'name': 'SKYSAT2', 'metric': 'Vegetation Classification'},
        {'id': '13A14', 'name': 'WORLDVIEW3', 'metric': 'Sea Salinity'},
        {'id': '6N14', 'name': 'ASNARO1', 'metric': 'Sea Salinity'},
    ]
    for satellite in def_satellites:
        sat = Satellite(**satellite)
        session.add(sat)
    try:
        session.commit()
    except db.exc.IntegrityError:
        session.rollback()


def import_sat_data(csv_filenames, session_override=None):
    """Import satellite data from CSV files.

    A list of files can be imported in one command, and this
    will add all the data to the `satellite_data` table.

    A session_override is included in the case of importing
    from the command line. A new database session needs to
    be instantiated in order for this to access the database.

    The CSV file must be in the exact format (with semicolon
    delimiters and the datetime as MM-DD-YYYY HH:MI) in order
    for this to work.

    The `file_import` table is updated with the details of the
    filename and when the import started and finished.
    """
    if session_override:
        session = session_override

    for csv_filename in csv_filenames:
        file_import = FileImport(
            filename=csv_filename,
            start_dt=datetime.now(),
        )
        session.add(file_import)
        session.commit()

        with open(csv_filename) as csv_file:
            reader = csv.DictReader(csv_file, delimiter=';')
            for row in reader:
                measurement = SatelliteData(
                    satellite_id=row['idSat'],
                    file_import_id=file_import.id,
                    measurement_dt=datetime.strptime(row['timestamp'], '%m-%d-%Y %H:%M'),
                    ionosphere=row['ionoIndex'],
                    ndvi=row['ndviIndex'],
                    radiation=row['radiationIndex'],
                    measurement=row['specificMeasurement'],
                )
                session.add(measurement)

        session.commit()

        file_import.end_dt = datetime.now()
        session.commit()