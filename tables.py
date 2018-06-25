from app.storage.base import init_db, drop_tables, Base
import sys


def create_or_drop_all(sysarg):
    if sysarg == 'create':
        dbName = init_db()
        print('Created all Tables in %s' %(dbName))
    elif sysarg == 'drop':
        dbName = drop_tables()
        print('Dropped all Tables from %s' %(dbName))
    else:
        print("Usage: python tables.py <create | drop>")


if __name__ == '__main__':
    try:
        sysarg = sys.argv[1]
    except IndexError:
        print("Usage: python tables.py <create | drop>")
        quit()

    create_or_drop_all(sysarg)
