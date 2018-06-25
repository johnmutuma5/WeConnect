from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import MetaData
from app import config

dbEngine = create_engine(config['SQLALCHEMY_DATABASE_URI'])
dbName = str(dbEngine.url).split('/')[-1]

convention = config.get('NAMING_CONVENTION')
meta = MetaData(naming_convention=convention)
Base = declarative_base(metadata=meta)

def weconnect_table_names():
    all_tables = [table.name for table in Base.metadata.tables.values()]
    return all_tables


def init_db():
    Base.metadata.create_all(bind=dbEngine)
    print(Base.metadata.tables['business'].insert())
    return dbName


def drop_tables():
    Base.metadata.drop_all(bind=dbEngine)
    return dbName
