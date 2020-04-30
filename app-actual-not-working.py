"""
UI built using dash to perform basic tasks like uploading user data and setting proper parameters.
"""


import base64
import datetime
import io
import os
import sys
import pandas as pd

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table

# import local modules

module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path+'\\foresee\\foresee\\scripts')

#import main


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

input_data_columns = list()

app.layout = html.Div([
    
    ### prompt user to provide id column(s) name(s) ###
    
    dcc.Markdown('''
    **If uploading more than one time series then you need to provide an id column name.**
    '''),
    dcc.Input(id="id-column", type="text", placeholder=""),
    html.Br(),   
    
    ### prompt user to provide date_stamp column name ###
    
    dcc.Markdown('''
    **provide date stamp column name if available.**
    '''),
    dcc.Input(id="ds-column", type="text", placeholder=""),
    html.Br(),   
    
    ### prompt user to provide time series frequency ###
    
    dcc.Markdown('''
    **provide time series frequency, default is 12.**
    '''),
    dcc.Input(id="ts-freq", type="number", placeholder=12),
    html.Br(),   
    
    ### prompt user to provide forecast length ###
    
    dcc.Markdown('''
    **provide forecast length, default is 10.**
    '''),
    dcc.Input(id="fcst-length", type="number", placeholder=10),
    html.Br(),   
    
    ### display available output formats ###

    dcc.Markdown('''
    **Select result output format.**
    '''),
    dcc.RadioItems(
        id='result-format',
        options=[
            {'label': 'Best Model', 'value': 'best_model'},
            {'label': 'All Models', 'value': 'all_models'},
            {'label': 'All & Best', 'value': 'all_best'}
        ],
        value='all_models',
        labelStyle={'display': 'inline-block'}
    ),
    html.Br(),   
    
    ### prompt user to provide holdout length ###
    
    dcc.Markdown('''
    **If comparing model results provide holdout length for out of sample
    forecast accuracy estimation. default is 5.**
    '''),
    dcc.Input(id="holdout-length", type="number", placeholder=5),
    html.Br(),   
    
    # display model list

    html.H5('Select or Remove Models'),
    
    dcc.Checklist(
        id='model-options',
        options=[
            {'label': 'EWM', 'value': 'ewm_model'},
            {'label': 'FFT', 'value': 'fft'},
            {'label': 'Holt Winters', 'value': 'holt_winters'},
            {'label': 'Prophet', 'value': 'prophet'},
            {'label': 'Sarimax', 'value': 'sarimax'}
        ],
        value=['ewm_model', 'fft', 'holt_winters', 'prophet', 'sarimax'],
        labelStyle={'display': 'inline-block'}
    ),
    
    html.Hr(),
    
    ### upload file box ###
    
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
        multiple=True
    ),
    
    ### display a sample of input data ###
    
    html.Div(id='output-sample-data', style={'width': '50%'}),
    html.Br(),   
    
    ### display result ###
    
    html.Div(
        id='output-result',
        style={'width': '50%'}
    ),
    html.Hr(),
    
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
    
    df_info = [col + ': ' + str(content[col].dtype) for col in content.columns]
    df_info = '\n'.join([s for s in df_info])
    
    if type(content) == str :
        return html.Div([err])
    
    else:
        return html.Div([
            #TODO: fix linebreak
            dcc.Markdown(df_info),

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

    
@app.callback(Output('output-sample-data', 'children'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename')])

def update_output(list_of_contents, list_of_names):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n) for c, n in
            zip(list_of_contents, list_of_names)]
        return children
    
    
@app.callback(Output('output-result', 'children'),
              [
                  Input('id-column', 'value'),
                  Input('ds-column', 'value'),
                  Input('ts-freq', 'value'),
                  Input('fcst-length', 'value'),
                  Input('result-format', 'value'),
                  Input('holdout-length', 'value'),
                  Input('model-options', 'value'),
                  Input('upload-data', 'contents'),
              ],
              [State('upload-data', 'filename')])

def parse_result(gbkey, ds_column, freq, fcst_length, run_type, holdout_length, model_list, contents, filename):
    if contents is not None:
        try:
            df_list = [read_contents(c, f) for c,f in zip(contents, filename)]
            raw_fact = df_list[0]
            
            result, fit_result_list = main.collect_result(
                                            raw_fact,
                                             gbkey,
                                             ds_column, 
                                             freq, 
                                             fcst_length, 
                                             run_type, 
                                             holdout_length, 
                                             model_list
                                        )

            return display_dataframe(result, 'forecast result')
        
        except Exception as e:
            return 'run failed with err: ' + str(e)
    
    
    
    
if __name__ == '__main__':
    app.run_server(debug=True)