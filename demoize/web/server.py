# all the imports
from flask import Flask, render_template

# configuration
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)

PARAMS = {
    'title': "Demoize Server",
    'heading': "Demoize Test",
    'code': 'var x = 1;',
}


@app.route('/')
def index():
    return render_template('index.html', **PARAMS)


def run_app(port=5000, **kwargs):
    global PARAMS
    PARAMS.update(kwargs)
    app.run(port=port)


if __name__ == '__main__':
    app.run()
