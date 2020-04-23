
#https://dash.plotly.com/dash-core-components/upload
# import os
# os.chdir('C:\\Users\\abc_h\\Desktop\\github\\foresee\\foresee')


import base64
import datetime
import io
import pandas as pd

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table

import main

# ts_results = main.collect_result()
# sm_name = list(ts_results[1])
sm_name = 'main is not running'


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
    
    html.H5('Select or Remove Models'),
    
    dcc.Checklist(
        id='model-options',
        options=[
            {'label': 'FFT', 'value': 'fft'},
            {'label': 'Holt Winters', 'value': 'holt_winters'},
            {'label': 'Sarimax', 'value': 'sarimax'}
        ],
        value=['fft', 'holt_winters', 'sarimax'],
        labelStyle={'display': 'inline-block'}
    ),
    
    html.Div(id='model-list', style={'width': '50%'}),
    html.Hr(),
    
    html.Div(id='output-result', style={'width': '50%'}),
    html.Hr(),
    dcc.Markdown(children=sm_name),
    
])

### read user input
def read_contents(contents, filename):
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
            
        return df
        
    except Exception as e:
        return str(e)

### display user input
def parse_contents(contents, filename):
    
    content = read_contents(contents, filename)
    
    if type(content) == str :
        return html.Div([err])
    
    else:
        return html.Div([
            html.H5(filename),

            dash_table.DataTable(

                data=content.head(3).to_dict('records'),

                columns=[{'name': i, 'id': i} for i in content.columns],
            ),
            html.Hr(),
        ])
    

### display dataframe
def display_dataframe(df, name):
    
    if df is None:
        return html.Div(['there is no dataframe to display'])
        
    else:
        return html.Div([
            html.H5(name),
            dash_table.DataTable(
                data=df.to_dict('records'),
                columns=[{'name': i, 'id': i} for i in df.columns],
            ),
            html.Hr(),
        ])

    
@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename')])

def update_output(list_of_contents, list_of_names):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n) for c, n in
            zip(list_of_contents, list_of_names)]
        return children

    
    
@app.callback(Output('model-list', 'children'),
              [Input('model-options', 'value')])

def parse_selected_models(model_list):
    
    if model_list is not None:
        return 'number of selected stat models: ' + str(len(model_list))
    else:
        return 'model_list is None'
    

@app.callback(Output('output-result', 'children'),
              [Input('upload-data', 'contents'),
              Input('model-options', 'value')],
              [State('upload-data', 'filename')])

def parse_result(contents, model_list, filename):
    if contents is not None:
        try:
            df_list = [read_contents(c, f) for c,f in zip(contents, filename)]
            raw_fact = df_list[0]
            model_list = model_list

            result = main.collect_result(raw_fact, model_list)

            return display_dataframe(result, 'forecast result')
        
        except Exception as e:
            return 'run failed with err: ' + str(e)
    
    
    
    
if __name__ == '__main__':
    app.run_server(debug=True)