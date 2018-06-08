from flask import render_template

def index():
    ctx = {
        'title': 'WeConnect - Homepage'
    }
    return render_template('index.html', **ctx), 200


def documentation():
    return render_template('documentation.html'), 200
