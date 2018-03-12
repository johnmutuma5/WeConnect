#! venv/bin/python
from app import app

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('127.0.0.1', 8080, app, use_debugger=True, use_reloader=True)
    # app.run ()
