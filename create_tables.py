from app.v2 import dbEngine
from app.v2.models import Base

Base.metadata.create_all (dbEngine)
# Base.metadata.drop_all (dbEngine)
