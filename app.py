
"""
UI built using dash to perform basic tasks like uploading user data and setting proper parameters.
"""

from foresee.webapp.layout import app_layout
from foresee.webapp.callbacks import register_callbacks
import dash_bootstrap_components as dbc

import flask
import dash

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', dbc.themes.BOOTSTRAP]

app = dash.Dash(
					__name__,
					external_stylesheets=external_stylesheets,
					suppress_callback_exceptions=True
				)

server = app.server

app.layout = app_layout

register_callbacks(app)



if __name__ == '__main__':
    app.run_server(debug=True)