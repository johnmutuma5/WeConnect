from app.storage.facades import UserDbFacade
from app.storage.base import dbEngine

userDbFacade = UserDbFacade(dbEngine)
