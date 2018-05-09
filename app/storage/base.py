from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import MetaData
from app import config

dbEngine = create_engine(config['SQLALCHEMY_DATABASE_URI'])

convention = config.get('NAMING_CONVENTION')
meta = MetaData(naming_convention=convention)
Base = declarative_base(metadata=meta)


def init_db():
    Base.metadata.create_all(bind=dbEngine)


def drop_tables():
    Base.metadata.drop_all(bind=dbEngine)
