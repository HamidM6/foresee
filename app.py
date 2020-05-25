# run this command
import flask
import dash

server = flask.Flask(__name__)

@server.route('/')
def index():
    return 'Flask root.'

from foresee.webapp.dash_app import app

if __name__ == '__main__':
    app.run_server()
    