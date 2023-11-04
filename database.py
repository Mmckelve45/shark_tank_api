from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'
# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Testme321!@localhost/TodoApplicationDatabase'
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Testme321!@localhost/SharkTankDB'

# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})
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