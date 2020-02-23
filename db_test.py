import os

import sqlalchemy as db

from __init__ import db_session
from models import (
    Base,
    FileImport,
    Satellite,
    SatelliteData,
    add_satellites,
    import_sat_data,
)


database_uri = os.environ.get('MYSQL_DATABASE_URI')
try:
    engine = db.create_engine(database_uri, echo=True)
except TypeError:
    raise AttributeError('DB engine could not be initialized')

Base.metadata.create_all(engine)
add_satellites(db_session)
import_sat_data(['satDataCSV2.csv'], db_session)