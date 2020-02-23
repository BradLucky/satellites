import sys

from __init__ import db_session
from models import import_sat_data


if __name__ == '__main__':
    print('Importing data from stdin')
    import_sat_data(sys.argv[1:], db_session)
    print('Done importing')
