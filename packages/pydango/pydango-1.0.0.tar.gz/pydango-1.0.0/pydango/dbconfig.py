"""Get config variables from config.ini file to help us connect to PostgreSQL database"""

from importlib import resources

from configparser import ConfigParser

def read_db_config(filename='config.ini', section='postgresql'):
    """Read database configuration file and return a dictionary object"""

    # create parser and read ini configuration file
    parser = ConfigParser()
    parser.read_string(resources.read_text("pydango", "config.ini"))

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1]
    else:
        raise Exception(f"{section} not found in the {filename} file")

    return db






