from app import app
from flask import render_template

@app.route('/', methods=['GET'])
def index():
    ctx = {
        'title': 'WeConnect - Homepage'
    }
    return render_template('index.html', **ctx)


@app.route('/api/documenation', methods=['GET'])
def documentation():
    return render_template('documentation.html')
