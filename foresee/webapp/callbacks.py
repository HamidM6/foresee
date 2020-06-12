
from foresee.scripts import main
from foresee.webapp.layout import intro_layout, main_layout

import base64
import datetime
import io
import os
import sys
import pandas as pd

import flask
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table



### read user input
def read_contents(contents, ds_colname, filename):

	try:
		content_type, content_string = contents.split(',')
		decoded = base64.b64decode(content_string)

		if 'csv' in filename:
			# Assume that the user uploaded a CSV file
			df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))

			if ds_colname in df.columns:
				df[ds_colname] = pd.to_datetime(df[ds_colname])

			return df

		elif 'xls' in filename:
			# Assume that the user uploaded an excel file
			df = pd.read_excel(io.BytesIO(decoded))

			if ds_colname in df.columns:
				df[ds_colname] = pd.to_datetime(df[ds_colname])

			return df

		else:
			# TODO: update this to read txt file
			# Assume that the user uploaded a txt file
			df = pd.read_csv(
				io.StringIO(decoded.decode('utf-8'))
			)
			if ds_colname in df.columns:
				df[ds_colname] = pd.to_datetime(df[ds_colname])

			return df

	except Exception as e:
		return str(e)

### display user input
def parse_contents(contents, ds_colname, filename):

	content = read_contents(contents, ds_colname, filename)

	if type(content) == type(pd.DataFrame()):
		try:
			df_info = [col + ': ' + str(content[col].dtype) for col in content.columns]
			df_info = [x + ' *** ' for x in df_info]
			df_info = '\n'.join([s for s in df_info])

			return html.Div([
				#TODO: fix linebreak
				dcc.Markdown(df_info),

				html.H6('Input data: ' + filename),
				dash_table.DataTable(

					data=content.to_dict('records'),
					columns=[{'name': i, 'id': i} for i in content.columns],
					page_action='none',
					style_table={'height': '200px', 'overflowY': 'auto'},

				),
				html.Hr(),
			])

		except Exception as e:
			return html.H6('Failed to display input data: ' + str(e))


	else:
		return html.H6('Failed to read input data: ' + content)


### display dataframe
def display_dataframe(df, name):

	if type(df) == type(pd.DataFrame()):
		return html.Div([
			html.H5(name),
			dash_table.DataTable(
				data=df.to_dict('records'),
				columns=[{'name': i, 'id': i} for i in df.columns],
				page_action='none',
				style_table={'height': '300px', 'overflowY': 'auto'},              
				export_columns = 'all',
				export_format = 'csv',
			),
			html.Hr(),
		])

	else:
		return html.Div(['run failed with error : ' + str(df)])



def register_callbacks(app):
    ### read input file, display a sample
    @app.callback(Output('output-sample-data', 'children'),
                [
                    Input('upload-data', 'contents'),
                    Input('ds-column', 'value'),
                ],
                [
                    State('upload-data', 'filename'),
                ])

    def update_output(content_list, ds_colname, filename_list):

        if content_list is not None:
            return  parse_contents(content_list[0], ds_colname, filename_list[0])
        else:
            return

    ### tab-click actions
    @app.callback(Output('tabs-content', 'children'),
                [Input('tab-collection', 'value')])

    def render_content(tab):
        if tab == 'tab-1':
            return intro_layout

        elif tab == 'tab-2':
            return main_layout
            

    ### varify sarimax order input
    @app.callback(
        Output("sarimax-order-output", "children"),
        [Input('sarimax-order-input', 'value')],
    )
    def varify_display_order(input):
        return str(input)


    ### read input file and parameters, display forecast results
    @app.callback(Output('output-result', 'children'),
                [
                    Input('endog-column', 'value'),
                    Input('id-column', 'value'),
                    Input('ds-column', 'value'),
                    Input('ts-freq', 'value'),
                    Input('fcst-length', 'value'),
                    Input('result-format', 'value'),
                    Input('holdout-length', 'value'),
                    Input('model-options', 'value'),
                    Input('upload-data', 'contents'),
                    Input('fit-execution-method', 'value'),
                    Input('tune-params', 'value'),
                    Input('sarimax-order-input', 'value'),
                ],
                [State('upload-data', 'filename')])

    def parse_result(
                        endog_colname,
                        gbkey,
                        ds_colname,
                        freq,
                        fcst_length,
                        run_type,
                        holdout_length,
                        model_list,
                        content_list,
                        processing_method,
                        param_type,
                        sarimax_order,
                        filename_list,
                    ):
        
        if content_list is not None:
            try:
                
                raw_fact = read_contents(content_list[0], ds_colname, filename_list[0])
                raw_fact_cols = raw_fact.columns
                
                if gbkey not in raw_fact_cols:
                    gbkey = 'id'
                if ds_colname not in raw_fact_cols:
                    ds_colname = 'date_stamp'
                if freq == '':
                    freq = 1
                if fcst_length == '':
                    fcst_length = 10
                if holdout_length == '':
                    holdout_length = 5
                if param_type == 'tune':
                    tune = True
                else:
                    tune = False

                if sarimax_order is not None:
                    args = {'sarimax_order': sarimax_order}
                    
                result, fit_result_list = main.collect_result(
                                                                            raw_fact,
                                                                            endog_colname,
                                                                            gbkey,
                                                                            ds_colname,
                                                                            freq,
                                                                            fcst_length,
                                                                            run_type,
                                                                            holdout_length,
                                                                            model_list,
                                                                            processing_method,
                                                                            tune,
                                                                    )
                return display_dataframe(result, 'forecast result')
                
            except Exception as e:
                return display_dataframe(str(e), None)
