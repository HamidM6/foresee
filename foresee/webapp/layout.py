
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc


# app layout
app_layout = dbc.Container([
	dcc.Tabs(id='tab-collection', value='tab-1', children=[
		dcc.Tab(label='Introduction', value='tab-1'),
		dcc.Tab(label='Main', value='tab-2'),
	]),
	html.Div(id='tabs-content')
])

# intro layout
intro_layout = html.Div(
	[
		html.Br(),
		html.H3('NOTE'),
		html.Br(),
		dbc.Alert(
			[
				html.H5("UI and engine are under development so it's not stable and will be updated frequently."),
				html.H5("This app is hosted on heroku free trail and will not function properly with large data sets."),
			],
			color="warning"
				),
		html.Br(),
		dbc.Alert(
			[
				html.H2('User Guide'),
				html.Br(),
				html.H4('Input file needs to be in csv format and column name is required.'),
				html.H4('If file contains more than one time series, a time series id column is needed.'),
				html.H4('If file contains time series date-time index, a date-time column name is needed.'),
				html.H4('Time series frequency is import and default value (1) value may not be optimal.'),
				html.H4('Without tuning, model parameters are set to their default parameters.'),
				html.H4('With tuning, model parameters are set to maximize forecast accuracy for holdout period.'),
				html.Br(),
				html.H2('Output has the following formats'),
				html.Br(),
				html.H4('All Models: fitted values and forecast for all selected models without model comparison.'),
				html.H4('Best Model: fitted values and forecast for best model among select models and its forecast accuracy.'),
				html.H4('All & Best: fitted values and forecast for all selected models and their forecast accuracy and the best model.'),
			],
			color='primary'),
	]

)

# main layout
main_layout = html.Div([

	### prompt user to provide time series column name
	html.Div(
		[
			html.Br(),
			dbc.Row(
				[
					dbc.Col(
						dbc.Alert([html.H5("Provide time series values column name. Default is 'y'.")], color="primary"),
						align='left',
						width=9,
						),
					dbc.Col(
						dcc.Input(id='endog-column', type='text', placeholder='time series column', value='y'),
						align="right",
						width=2
						),
				],
			),
		]
	),

	### prompt user to provide id column name ###
	html.Div(
		[
			html.Br(),
			dbc.Row(
				[
					dbc.Col(
						dbc.Alert([html.H5("If uploading more than one time series, provide an id column name. Default is 'id'.")], color="primary"),
						align='left',
						width=9,
						),
					dbc.Col(
						dcc.Input(id='id-column', type='text', placeholder='time series id column', value='id'),
						align="right",
						width=2
						),
				],
			),
		]
	),

	### prompt user to provide date_stamp column name ###
	html.Div(
		[
			html.Br(),
			dbc.Row(
				[
					dbc.Col(
						dbc.Alert([html.H5("Provide date stamp column name if available. Default is 'date_stamp'.")], color="primary"),
						align='left',
						width=9,
						),
					dbc.Col(
						dcc.Input(id='ds-column', type='text', placeholder='Date-Time column', value='date_stamp'),
						align="right",
						width=2
						),
				],
			),
		]
	),

	### prompt user to provide time series frequency ###
	html.Div(
		[
			html.Br(),
			dbc.Row(
				[
					dbc.Col(
						dbc.Alert([html.H5("Provide time series frequency. Default is 1.")], color="primary"),
						align='left',
						width=9,
						),
					dbc.Col(
						dcc.Input(id='ts-freq', type='number', placeholder='time series frequency', value=1),
						align="right",
						width=2
						),
				],
			),
		]
	),

	### prompt user to provide forecast length ###
	html.Div(
		[
			html.Br(),
			dbc.Row(
				[
					dbc.Col(
						dbc.Alert([html.H5("Provide forecast length. Default is 10.")], color="primary"),
						align='left',
						width=9,
						),
					dbc.Col(
						dcc.Input(id='fcst-length', type='number', placeholder='forecast horizon', value=10),
						align="right",
						width=2
						),
				],
			),
		]
	),

	### prompt user to provide holdout length ###
	html.Div(
		[
			html.Br(),
			dbc.Row(
				[
					dbc.Col(
						dbc.Alert([html.H5("If comparing model results, provide holdout length for out of sample forecast accuracy estimation. Default is 5.")], color="primary"),
						align='left',
						width=9,
						),
					dbc.Col(
						dcc.Input(id='holdout-length', type='number', placeholder='out of sample holdout len', value=5),
						align="right",
						width=2
						),
				],
			),
		]
	),


	### display available output formats ###
	html.Div([
		html.Br(),
		dbc.Row(
			dbc.Col(
				dbc.Alert([html.H4('Select result output format.')], color="primary"),
				align='left',
				width=9,
			),
		),
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
	]),


	### display fit-forecast processing method (parallel/sequential) ###
	html.Div([
		html.Br(),
		dbc.Row(
			dbc.Col(
				dbc.Alert([html.H4('Select fit-forecast processing method. Parallel execution with "dask" library.')], color='primary'),
				align='left',
				width=9,
			),
		),
		dcc.RadioItems(
			id='fit-execution-method',
			options=[
				{'label': 'Parallel', 'value': 'parallel'},
				{'label': 'Sequential', 'value': 'non_parallel'}
			],
			value='non_parallel',
			labelStyle={'display': 'inline-block'}
		),
	]),

	### display model list ###
	html.Div([
		html.Br(),
		dbc.Row(
			dbc.Col(
				dbc.Alert([html.H4('Select or Remove Models')], color='primary'),
				align='left',
				width=9,
			),
		),
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
	]),


	### display input box for sarimax orders ###
	html.Div(
		[
			html.Br(),
			dbc.Row(
				[
					dbc.Col(
						dbc.Alert(
							[html.H4("Enter (p,d,q) values of sarimax (optional).")],
							color="primary"
							),
							align='left',
							width=9,
						),
					dbc.Col(
						dcc.Input(id='sarimax-order-input', type='text', placeholder='1,1,1'),
						align='right',
						width=2,
					),
				],
			),
		]
	),


	### display model parameter tuning option ###
	html.Div([
		html.Br(),
		dbc.Row(
			dbc.Col(
				dbc.Alert(
					[html.H4('If tune is selected, model parameters will be optimized using holdout forecast accuracy.')],
					color='primary',
				),
				align='left',
				width=9,
			),
		),
		dcc.RadioItems(
			id='tune-params',
			options=[
				{'label': 'Tuned Parameters', 'value': 'tune'},
				{'label': 'Default Parameters', 'value': 'default'}
			],
			value='default',
			labelStyle={'display': 'inline-block'}
		),
	]),


	### upload file box ###
	dcc.Upload(
		id='upload-data',
		children=html.Div([
			html.H6('Column name (header) is required!!!'),
			'Drag and Drop or ',
			html.A('Select Files'),
		]),
		style={
			'width': '50%',
			'height': '100px',
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
	html.Div(
			dcc.Loading(
				id="loading-sample-input",
				type="circle",
				children=html.Div(id='output-sample-data', style={'width': '50%'})
			)
	),

	### display final result dataframe ###
	html.Div(
			dcc.Loading(
				id="loading-result",
				type="circle",
				children=html.Div(id='output-result', style={'width': '50%'})
			)
	)
])
