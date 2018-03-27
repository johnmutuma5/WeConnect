from app.v2 import dbEngine
from app.v2.models import Base
import sys

def create_or_drop_all (sysarg):
    if sysarg == 'create':
        Base.metadata.create_all (dbEngine)
        print('Created Tables')
    elif sysarg == 'drop':
        Base.metadata.drop_all (dbEngine)
        print('Dropped Tables')
    else:
        print("Usage: python tables.py <create | drop>")


if __name__ == '__main__':
    try:
        sysarg = sys.argv[1]
    except IndexError:
        print("Usage: python tables.py <create | drop>")
        quit()

    create_or_drop_all (sysarg)
