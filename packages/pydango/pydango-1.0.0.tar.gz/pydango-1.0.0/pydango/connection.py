
from sqlalchemy import create_engine

from pydango import dbconfig

db_config = dbconfig.read_db_config()

database_url = f"""postgresql://{db_config['user']}:{db_config['password']}\
@{db_config['host']}:{db_config['port']}/{db_config['database']}"""

def create_connection():
    """Connect to postgresql through SQLAlchemy"""
    engine = create_engine(database_url)

    return engine



