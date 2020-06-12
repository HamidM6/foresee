
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

import base64
import datetime
import io
import os
import sys
import json
import pandas as pd

import flask
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
from dash.exceptions import PreventUpdate


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', dbc.themes.BOOTSTRAP]

app = dash.Dash(
					__name__,
					external_stylesheets=external_stylesheets,
					suppress_callback_exceptions=True
				)
				
server = app.server



### upload file box
upload_file_box = dcc.Upload(
			id='upload-data',
			children=[html.A('Select a file.')],
			style={
				'width': '100%',
				'height': '100px',
				'lineHeight': '60px',
				'borderWidth': '1px',
				'borderStyle': 'dashed',
				'borderRadius': '5px',
				'textAlign': 'center',
				'margin': '10px'
			},
)


### columns name menu box
# colnames = ['x', 'y', 'z']
# controls = dbc.Card(
#     [
#         dbc.FormGroup(
#             [
#                 dbc.Label("time series ID column"),
#                 dcc.Dropdown(
#                     id="id-column",
#                     options=[
#                         {"label": col, "value": col} for col in colnames
#                     ],
#                     value="id",
#                 ),
#             ]
#         ),
#         dbc.FormGroup(
#             [
#                 dbc.Label("date stamp column"),
#                 dcc.Dropdown(
#                     id="ds-column",
#                     options=[
#                         {"label": col, "value": col} for col in colnames
#                     ],
#                     value="date_stamp",
#                 ),
#             ]
#         ),
#         dbc.FormGroup(
#             [
#                 dbc.Label("time series"),
#                 dcc.Dropdown(
#                     id="endog-column",
#                     options=[
#                         {"label": col, "value": col} for col in colnames
#                     ],
#                     value="y",
#                 ),
#             ]
#         ),
#     ],
#     body=True,
# )



### app layout
app.layout = html.Div([
    dcc.Store(id='data-memory'),
    dcc.Store(id='column-memory'),
    dbc.Container([
        html.Br(),
        html.H1('Drop a file and identify columns.'),
        dbc.Row([
            dbc.Col(upload_file_box),
            dbc.Col(id='identify-columns'),
        ], align='center'),
        html.Hr(),
        html.Div(id='print-columns')
    ],
    fluid=True,
    )
])


### read user input
def read_contents(contents, filename):

	try:
		content_type, content_string = contents.split(',')
		decoded = base64.b64decode(content_string)

		if 'csv' in filename:
			# Assume that the user uploaded a CSV file
			df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))

			return df

		elif 'xls' in filename:
			# Assume that the user uploaded an excel file
			df = pd.read_excel(io.BytesIO(decoded))


			return df

		else:
			# TODO: update this to read txt file
			# Assume that the user uploaded a txt file
			df = pd.read_csv(
				io.StringIO(decoded.decode('utf-8'))
			)

			return df

	except Exception as e:
		return str(e)


### read input file, store in memory
@app.callback(
    Output('data-memory', 'data'),
    [
        Input('upload-data', 'contents')
    ],
    [
        State('upload-data', 'filename')
    ]

)

def load_file_save_data(contents, filename):
    if contents is not None:
        df = read_contents(contents, filename)
        return df.to_json()





### read input file, display columns with dropdown menu
@app.callback(
    Output('identify-columns', 'children'),
    [
        Input('data-memory', 'data'),
    ],
)

def identify_columns(data):

    if data is None:
        raise PreventUpdate

    else:
        df = pd.DataFrame.from_dict(json.loads(data), orient='columns')
        colnames = [c for c in df.columns]
        controls = dbc.Card(
            [
                dbc.FormGroup(
                    [
                        dbc.Label("time series ID column"),
                        dcc.Dropdown(
                            id="id-column",
                            options=[
                                {"label": col, "value": col} for col in colnames
                            ],
                            value="id",
                        ),
                    ]
                ),
                dbc.FormGroup(
                    [
                        dbc.Label("date stamp column"),
                        dcc.Dropdown(
                            id="ds-column",
                            options=[
                                {"label": col, "value": col} for col in colnames
                            ],
                            value="date_stamp",
                        ),
                    ]
                ),
                dbc.FormGroup(
                    [
                        dbc.Label("time series"),
                        dcc.Dropdown(
                            id="endog-column",
                            options=[
                                {"label": col, "value": col} for col in colnames
                            ],
                            value="y",
                        ),
                    ]
                ),
            ],
            body=True,
        )

    return controls



### store column names in memory
@app.callback(
    Output('columns-memory', 'data'),
    [
        Input('data-memory', 'data')
    ]
)

def identify_columns(data):

    if data is None:
        raise PreventUpdate

    else:
        df = pd.DataFrame.from_dict(json.loads(data), orient='columns')
        colnames = [c for c in df.columns]
        controls = dbc.Card(
            [
                dbc.FormGroup(
                    [
                        dbc.Label("time series ID column"),
                        dcc.Dropdown(
                            id="id-column",
                            options=[
                                {"label": col, "value": col} for col in colnames
                            ],
                            value="id",
                        ),
                    ]
                ),
                dbc.FormGroup(
                    [
                        dbc.Label("date stamp column"),
                        dcc.Dropdown(
                            id="ds-column",
                            options=[
                                {"label": col, "value": col} for col in colnames
                            ],
                            value="date_stamp",
                        ),
                    ]
                ),
                dbc.FormGroup(
                    [
                        dbc.Label("time series"),
                        dcc.Dropdown(
                            id="endog-column",
                            options=[
                                {"label": col, "value": col} for col in colnames
                            ],
                            value="y",
                        ),
                    ]
                ),
            ],
            body=True,
        )

    return controls


### test object in memory
### call stored data, display columns
@app.callback(
    Output('print-columns', 'children'),
    [
        Input('data-memory', 'data'),
    ]
)

def return_cols(data):
    if data is not None:
        df = pd.DataFrame.from_dict(json.loads(data), orient='columns')
        return df.columns





# ### test column names
# @app.callback(
#     Output('output-table-columns', 'children'),
#     [
#         Input('identify-columns', 'children')
#     ]
# )

# def display_id_column(contents):
#     return html.Div(contents)




if __name__ == '__main__':
    app.run_server(debug=True)
