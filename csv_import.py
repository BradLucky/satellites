"""Easy access point for importing a CSV file.

This should be called from within the Flask Docker container
with the filename(s) as space-separated parameters.
"""
import sys

from app import db_session
from models import import_sat_data


if __name__ == '__main__':
    print('Importing data from stdin')
    import_sat_data(sys.argv[1:], db_session)
    print('Done importing')
