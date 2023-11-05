from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'

# Load the data with SQLite localDB
# - Please note if you do this you need to change the Arrays in the models file to be a different representation
# SQLite does not support array types
# SQLALCHEMY_DATABASE_URL = 'sqlite:///./sharktankapp.db'
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Testme321!@localhost/TodoApplicationDatabase'

# Load the data with postgres localDB - create a Server/DB in postgres and give it a password
# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Testme321!@localhost/SharkTankDB'
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# from sqlalchemy import URL, create_engine
#
# connection_string = URL.create(
#   'postgresql',
#   username='Mmckelve45',
#   password='WpNaVvFR8oC4',
#   host='ep-soft-unit-44308222.cloud.argon.aws.neon.build',
#   database='SharkTankDB',
# )
#
# engine = create_engine(connection_string)