# run this command
import flask
import dash

from foresee.webapp.dash_app import app

server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server)

# @server.route('/')
# def index():
    # return 'Flask root.'


if __name__ == '__main__':
    app.run_server()
    