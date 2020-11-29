# Import Dash dependencies
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

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
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="crossfilter-indicator-scatter"),
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
    ]
)
def plot_scatter(x, y, date):
    cdf = owid_covid.df[owid_covid.df["date"]==date]

    x_1 = owid_covid.convert_to_original(x)
    y_1 = owid_covid.convert_to_original(y)

    fig = px.scatter(cdf, x=x_1, y=y_1, hover_name="location", labels={
                        x_1:x,
                        y_1:y
                    }
    )
    return fig

