# Import Dash dependencies
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Import bootstrap components
import dash_bootstrap_components as dbc

# Import pages/apps
from app import app

# Import data analysis dependencies
import pandas as pd
import plotly.express as px
from dateutil.relativedelta import relativedelta
import time
import datetime as dt
from dateutil.relativedelta import relativedelta
import plotly.graph_objects as go

##############################################################################

df = pd.read_csv('https://covid.ourworldindata.org/data/owid-covid-data.csv')
df = df

dff1 = None

df["date"] = pd.to_datetime(df["date"], infer_datetime_format=True).values
daterange = pd.date_range(start=df["date"].min(),end=df["date"].min(),freq='M')

def unixTimeMillis(dt):
    ''' Convert datetime to unix timestamp '''
    return int(time.mktime(dt.timetuple()))

def unixToDatetime(unix):
    ''' Convert unix timestamp to datetime. '''
    #return pd.to_datetime(unix,unit='s').dt.date
    return pd.to_datetime(pd.Series(unix), unit="s")


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

epoch = dt.datetime.utcfromtimestamp(0)

def unix_time_millis(d):
    return (d - epoch).total_seconds() #* 1000.0

available_indicators = df.columns

#############################################################################

layout = html.Div([
    dbc.Row(
        html.H3('COVID-19 Analysis Tool'),
        #width={"size":"auto"},
        justify="center", align="center",
    ),
    dbc.Row(
        html.P('This tool provides the user with the possibility of do an extensive analysis of the pandemics effect in all countries contained in the OWID dataset.'),
        justify="center", align="center",
    ),
    dbc.Row([
        dbc.Button("Primary", outline=True, color="primary", className="mr-1"),
        dbc.Button(
            "Secondary", outline=True, color="primary", className="mr-1"
        ),
        dbc.Button("Success", outline=True, color="primary", className="mr-1"),
        dbc.Button("Warning", outline=True, color="primary", className="mr-1"),
        dbc.Button("Danger", outline=True, color="primary", className="mr-1"),
        dbc.Button("Info", outline=True, color="primary", className="mr-1"),
        dbc.Button("Light", outline=True, color="primary", className="mr-1"),
        dbc.Button("Dark", outline=True, color="primary"),
        
    ], justify="center", align="center",),
    html.Br(),

    html.Div([

        html.Div([
            dcc.Dropdown(
                id='crossfilter-xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='total_deaths_per_million'
            )
            #dcc.RadioItems(
            #    id='crossfilter-xaxis-type',
            #    options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
            #    value='Log',
            #    labelStyle={'display': 'inline-block'}
            #)
        ],
        style={'width': '49%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='crossfilter-yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='total_cases_per_million'
            )
            #dcc.RadioItems(
            #    id='crossfilter-yaxis-type',
            #    options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
            #    value='Linear',
            #    labelStyle={'display': 'inline-block'}
            #)
        ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
    }),

    html.Div([
        dcc.Graph(
            id='crossfilter-indicator-scatter',
            hoverData={'points': [{'customdata': 'SWE'}]}
        )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
    html.Div([
        dcc.Graph(id='x-time-series'),
        dcc.Graph(id='y-time-series'),
    ], style={'display': 'inline-block', 'width': '49%'}),

    html.Div(dcc.Slider(
        id='crossfilter-year--slider',
        min=unix_time_millis(df['date'].min()),
        max=unix_time_millis(df['date'].max()),
        value=unix_time_millis(df['date'].max()),
        marks={unix_time_millis(year): {'label': str(year)} for year in df['date'].drop_duplicates()},
        step=None, 
        tooltip = { 'always_visible': False }
    ), style={'width': '49%', 'padding': '0px 20px 20px 20px'}),
    html.Div([
        dcc.Graph(id="world-map")
    ], style={'width': '90%', 'display': 'inline-block', 'padding': '0 20'})
])


@app.callback(
    Output('app-2-display-value', 'children'),
    [Input('app-2-dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)

@app.callback(Output('world-map', 'figure'),
    [Input('crossfilter-year--slider', 'value')])
def update_world_map(year_value):
    dff = df[df["date"] == unixToDatetime(year_value).iloc[0]]
    #fig = px.choropleth(dff, locations="iso_code", color="total_cases_per_million",
    #                    hover_name="location", color_continuous_scale=px.colors.sequential.thermal)


    fig = go.Figure(data=go.Choropleth(
        locations = dff['iso_code'],
        z = dff['total_cases_per_million'],
        text = dff['location'],
        colorscale = 'Blues',
        autocolorscale=False,
        reversescale=True,
        marker_line_color='darkgray',
        marker_line_width=0.5,
        #colorbar_tickprefix = '$',
        colorbar_title = 'Cases per million',
    ))

    fig.update_layout(
        title_text='Covid-19 Cases per million',
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='equirectangular'
        ),
        annotations = [dict(
            x=0.55,
            y=0.1,
            xref='paper',
            yref='paper',
            text='Source: <a href="https://github.com/owid/covid-19-data">\
                Our World in Data - Covid-19 Dataset</a>',
            showarrow = False
        )]
    )

    return fig 

@app.callback(
    Output('crossfilter-indicator-scatter', 'figure'),
    [Input('crossfilter-xaxis-column', 'value'),
     Input('crossfilter-yaxis-column', 'value'),
     Input('crossfilter-year--slider', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 year_value):
    print("Year: ", unixToDatetime(year_value).iloc[0])
    print("date: ", df["date"])
    dff = df[df["date"] == unixToDatetime(year_value).iloc[0]]
    #print("dff: ", dff)
    print(dff['population'])
    fig = px.scatter(x=dff[xaxis_column_name],
            y=dff[yaxis_column_name],
            hover_name=dff['location']
            )

    
    fig.update_traces(customdata=dff['location'])

    fig.update_xaxes(title=xaxis_column_name, type='linear')

    fig.update_yaxes(title=yaxis_column_name, type='linear')

    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

    return fig


def create_time_series(dff, title, column_name):
    
    fig = px.scatter(x=dff["date"], y=dff[column_name])

    fig.update_traces(mode='lines+markers')

    fig.update_xaxes(showgrid=False)

    fig.update_yaxes(type='linear')

    fig.add_annotation(x=0, y=0.85, xanchor='left', yanchor='bottom',
                       xref='paper', yref='paper', showarrow=False, align='left',
                       bgcolor='rgba(255, 255, 255, 0.5)', text=title)

    fig.update_layout(height=225, margin={'l': 20, 'b': 30, 'r': 10, 't': 10})

    return fig


@app.callback(
    Output('x-time-series', 'figure'),
    [Input('crossfilter-indicator-scatter', 'hoverData'),
     Input('crossfilter-xaxis-column', 'value')])
def update_y_timeseries(hoverData, xaxis_column_name):
    country_name = hoverData['points'][0]['customdata']
    dff = df[df['location'] == country_name]
    #dff = dff[xaxis_column_name]
    title = '<b>{}</b><br>{}'.format(country_name, xaxis_column_name)
    return create_time_series(dff, title, xaxis_column_name)


@app.callback(
    Output('y-time-series', 'figure'),
    [Input('crossfilter-indicator-scatter', 'hoverData'),
     Input('crossfilter-yaxis-column', 'value')])
def update_x_timeseries(hoverData, yaxis_column_name):
    dff = df[df['location'] == hoverData['points'][0]['customdata']]
    #dff = dff[yaxis_column_name]
    return create_time_series(dff, yaxis_column_name, yaxis_column_name)