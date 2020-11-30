# Import Dash dependencies
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

# Import bootstrap components
import dash_bootstrap_components as dbc

import pandas as pd
import plotly.express as px
from data import owid_covid

from dateutil.relativedelta import relativedelta
import time
import datetime

# Import pages/apps
from app import app

available_indicators = owid_covid.df.columns
daterange = owid_covid.daterange

# FROM https://stackoverflow.com/questions/51063191/date-slider-with-plotly-dash-does-not-work
def unixTimeMillis(dt):
    ''' Convert datetime to unix timestamp '''
    return int(time.mktime(dt.timetuple()))

# FROM https://stackoverflow.com/questions/51063191/date-slider-with-plotly-dash-does-not-work
def unixToDatetime(unix):
    ''' Convert unix timestamp to datetime. '''
    return pd.to_datetime(unix,unit='s')

# From https://stackoverflow.com/questions/51063191/date-slider-with-plotly-dash-does-not-work
def getMarks(start, end, Nth=100):
    ''' Returns the marks for labeling. 
        Every Nth value will be used.
    '''

    result = {}
    for i, date in enumerate(daterange):
        if(i%Nth == 1):
            # Append value to dict
            result[unixTimeMillis(date)] = str(date.strftime('%Y-%m-%d'))

    return result

layout = html.Div([
    dbc.Row(
        html.H3('COVID-19 Analysis Tool'),
        #width={"size":"auto"},
        justify="center", align="center",
    ),
    dbc.Row(
        html.P('Data used in this website is from OWID and OxCGRT'),
        justify="center", align="center",
    ),
    dbc.Row([
        dbc.Col([
            html.H6("X-axis"),
            dcc.Dropdown(
                id='crossfilter-xaxis-column',
                options=[{'label': i, 'value': i} for i in owid_covid.convert_to_readable(available_indicators)],
                value='Total deaths per million'
        )], width="3"),
        dbc.Col([
            html.H6("Date"),
            dcc.DatePickerSingle(
                id="picked_date",
                month_format='MMMM Y',
                placeholder='MMMM Y',
                date=datetime.date(2020,6,29)
            )  
        ], width="auto"),
        dbc.Col([
            html.H6("Y-axis"),    
            dcc.Dropdown(
                id='crossfilter-yaxis-column',
                options=[{'label': i, 'value': i} for i in owid_covid.convert_to_readable(available_indicators)],
                value='Total cases per million'
            )], width="3"),
        
    ], justify="center",  align="center"),
    html.Br(),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="crossfilter-indicator-scatter"),
        ],width="5"),
        dbc.Col([
                    
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Select(
                                            id='filter1',
                                            options=[{'label': i, 'value': i} for i in owid_covid.convert_to_readable(owid_covid.filters)],
                                            value='Median age'
                                ),
                            ], justify="center", align=""),
                            html.Br(),
                            dbc.Row([
                                dbc.Col([
                                    dbc.Select(
                                        id="operator1",
                                        options=[
                                            {"label": "Less than", "value": "less"},
                                            {"label": "Greater than", "value": "greater"},
                                        ],
                                        value="Less then"
                                    ),
                                ],width="4"),
                                dbc.Col([
                                    dbc.Input(
                                        id="filter1_input",
                                        type="number",
                                        value=100
                                    )
                                ],width="4"),
                                dbc.Col([
                                    dbc.Checklist(
                                        options=[
                                            {"label": "Apply", "value": 1},
                                        ],
                                        value=[],
                                        id="apply1",
                                    ),
                                ], width="4"),
                            ], justify="center", align="center"),

                        ])
                    ]),


                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Select(
                                            id='filter2',
                                            options=[{'label': i, 'value': i} for i in owid_covid.convert_to_readable(owid_covid.filters)],
                                            value='Population density'
                                ),
                            ], justify="center", align=""),
                            html.Br(),
                            dbc.Row([
                                dbc.Col([
                                    dbc.Select(
                                        id="operator2",
                                        options=[
                                            {"label": "Less than", "value": "less"},
                                            {"label": "Greater than", "value": "greater"},
                                        ],
                                        value="Less then"
                                    ),
                                ],width="4"),
                                dbc.Col([
                                    dbc.Input(
                                        id="filter2_input",
                                        type="number",
                                        value=100
                                    )
                                ],width="4"),
                                dbc.Col([
                                    dbc.Checklist(
                                        options=[
                                            {"label": "Apply", "value": 1},
                                        ],
                                        value=[],
                                        id="apply2",
                                    ),
                                ], width="4"),
                            ], justify="center", align="center"),

                        ])
                    ]),


                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Select(
                                            id='filter3',
                                            options=[{'label': i, 'value': i} for i in owid_covid.convert_to_readable(owid_covid.filters)],
                                            value='Life expectancy'
                                ),
                            ], justify="center", align=""),
                            html.Br(),
                            dbc.Row([
                                dbc.Col([
                                    dbc.Select(
                                        id="operator3",
                                        options=[
                                            {"label": "Less than", "value": "less"},
                                            {"label": "Greater than", "value": "greater"},
                                        ],
                                        value="Less then"
                                    ),
                                ],width="4"),
                                dbc.Col([
                                    dbc.Input(
                                        id="filter3_input",
                                        type="number",
                                        value=100
                                    )
                                ],width="4"),
                                dbc.Col([
                                    dbc.Checklist(
                                        options=[
                                            {"label": "Apply", "value": 1},
                                        ],
                                        value=[],
                                        id="apply3",
                                    ),
                                ], width="4"),
                            ], justify="center", align="center"),

                        ])
                    ]),
                
        ],width="5"),
    ],justify="center", align="center"),
    
    ])



@app.callback(
    Output('app-2-display-value', 'children'),
    [Input('app-2-dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)

@app.callback(
    Output("crossfilter-indicator-scatter", "figure"),
    [
        Input("crossfilter-xaxis-column", "value"),
        Input("crossfilter-yaxis-column", "value"),
        Input("picked_date", "date"),
        Input("apply1", "value"),
        Input("filter1", "value"),
        Input("operator1", "value"),
        Input("filter1_input", "value"),
        Input("apply2", "value"),
        Input("filter2", "value"),
        Input("operator2", "value"),
        Input("filter2_input", "value"),
        Input("apply3", "value"),
        Input("filter3", "value"),
        Input("operator3", "value"),
        Input("filter3_input", "value"),

    ]
)
def plot_scatter(x, y, date, val1, filter1, operator1, filter1_val, val2, filter2, operator2, filter2_val , val3, filter3, operator3, filter3_val ):

    cdf = owid_covid.df[owid_covid.df["date"]==date]

    filter1 = owid_covid.convert_to_original(filter1)
    filter2 = owid_covid.convert_to_original(filter2)
    filter3 = owid_covid.convert_to_original(filter3)

    if len(val1)>0:
        if operator1=="greater":
            cdf = cdf[cdf[filter1]>filter1_val]
        elif operator1=="less":
            cdf = cdf[cdf[filter1]<filter1_val]

    if len(val2)>0:
        if operator2=="greater":
            cdf = cdf[cdf[filter2]>filter2_val]
        elif operator1=="less":
            cdf = cdf[cdf[filter2]<filter2_val]

    if len(val3)>0:
        if operator3=="greater":
            cdf = cdf[cdf[filter3]>filter3_val]
        elif operator3=="less":
            cdf = cdf[cdf[filter3]<filter3_val]


    x_1 = owid_covid.convert_to_original(x)
    y_1 = owid_covid.convert_to_original(y)

    fig = px.scatter(cdf, x=x_1, y=y_1, hover_name="location", labels={
                        x_1:x,
                        y_1:y
                    }
    )
    return fig




   

