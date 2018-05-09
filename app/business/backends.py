from app.storage.facades import BusinessDbFacade
from app.storage.base import dbEngine

businessDbFacade = BusinessDbFacade(dbEngine)
