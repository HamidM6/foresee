
#https://dash.plotly.com/dash-core-components/upload
import base64
import datetime
import io

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table

import pandas as pd


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '50%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    
    html.Div(id='output-data-upload', style={'width': '50%'}),
    
    html.H5('Select or Drop Models'),
    
    dcc.Checklist(
        options=[
            {'label': 'FFT', 'value': 'fft'},
            {'label': 'Holt Winters', 'value': 'hw'},
            {'label': 'Sarimax', 'value': 'sarimax'}
        ],
        value=['fft', 'hw', 'sarimax'],
        labelStyle={'display': 'inline-block'}
    ),
    
    html.Div(id='output-data-name', style={'width': '50%'}),
    
])


def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),

        dash_table.DataTable(
                
            data=df.head(3).to_dict('records'),
            
            columns=[{'name': i, 'id': i} for i in df.columns],
        ),
        html.Hr(),  # horizontal line

    ])

def parse_names(filename):
    
    return html.Div([html.H6(filename)])


@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename')])

def update_output(list_of_contents, list_of_names):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n) for c, n in
            zip(list_of_contents, list_of_names)]
        return children

@app.callback(Output('output-data-name', 'children'),
              [Input('upload-data')],
              [State('filename')])

def update_output_div(list_of_names):
    return list_of_names

if __name__ == '__main__':
    app.run_server(debug=True)