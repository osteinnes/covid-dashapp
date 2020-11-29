# Import Dash dependencies
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate


# Import bootstrap components
import dash_bootstrap_components as dbc

# Import data analysis dependencies
import pandas as pd

import plotly.express as px

# Import data and utils
from data import owid_covid
from data import data_utils
from data import oxcgrt
import pycountry

# Import pages/apps
from app import app




country_layout = html.Div([
    # Graphs
    dbc.Row(
        html.H5("Pick a country"), justify="center", align="center",
    ),

    dbc.Row(
        dbc.Col(
            dbc.Select(
                    id='focus-country',
                    options=[{'label': i, 'value': i} for i in owid_covid.df["location"].unique()],
                    value='Norway'
                ), width="auto",
        ), justify="center", align="center"
    ),

    html.Br(),

    dbc.Row([
        html.Img(id="current-country-image"),
        html.H1(id="current-country"),
    ], justify="center", align="center"),

    html.Br(),

    dbc.Row([
            dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.H6(id="total-deaths", className="card-title"),
                    #html.P(id="total-deaths", className="card-text")
                ]),
            ), width=3),
            dbc.Col(
                dbc.Card(
                dbc.CardBody([
                    html.H6(id="total-cases", className="card-title"),
                    #html.Plaintext(id="total-cases")
                ]),
            ), width=3),
            dbc.Col(
                dbc.Card(
                dbc.CardBody([
                    html.H6(id="total-tests", className="card-title"),
                    #html.Plaintext(id="total-tests")
                ]),
            ), width=3)
            ],justify="center", align="center"),

    

    html.Br(),

    dbc.Row([
            dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.H6(id="population", className="card-title"),
                    #html.P(id="total-deaths", className="card-text")
                ]),
            ), width=3),
            dbc.Col(
                dbc.Card(
                dbc.CardBody([
                    html.H6(id="pop-dens", className="card-title"),
                    #html.Plaintext(id="total-cases")
                ]),
            ), width=3),
            dbc.Col(
                dbc.Card(
                dbc.CardBody([
                    html.H6(id="life-exp", className="card-title"),
                    #html.Plaintext(id="total-tests")
                ]),
            ), width=3),
    ],justify="center", align="center",
    ),

    html.Br(),
    
    dbc.Row([
        
        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.P("Select Y-axis"),
                            dbc.Select(id='y_axis_c',
                            value='Total deaths')
                            ], width="auto",
                        ),
                        dbc.Collapse(
                            dbc.Col([
                                html.P("Select policy"),
                                dbc.Select(
                                        id='restriction',
                                        options=[{'label': i, 'value': i} for i in oxcgrt.restrictions],
                                        value='None'
                                    )], width="auto",
                            ),
                            id="collapse"
                        )
                        ],justify="center", align="center",

                    ),
                    dbc.Collapse(
                        dbc.Row(
                            html.A("OxCGRT policy interpretation", id="srcc", href="https://github.com/OxCGRT/covid-policy-tracker/blob/master/documentation/codebook.md"),
                            justify="center", align="center"), id="collapse2"),
                    html.Br(),
                    dcc.Graph(id="country_graph"),
                    html.Div(id="graph_info"),
                    html.Div(id="graph_info2"),
                    html.Div(id="graph_info3"),
                    html.Div(id="graph_info4"),
                ]),
           )], width=9),



    ], justify="center", align="center"),

    html.Br(),

    dbc.Row([
        
        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.P("Select Y-axis"),
                            dbc.Select(id='y_axis_comparison',
                            options=[{'label': i, 'value': i} for i in owid_covid.convert_to_readable(owid_covid.y_axis_comparison)],
                            value='Total deaths per million')
                            ], width="4",
                        ),
                        dbc.Col([
                            html.P("Select Countries"),
                            dcc.Dropdown(
                                id='comparison-countries',
                                options=[{'label': i, 'value': i} for i in owid_covid.countries],
                                value='Norway',
                                multi=True
                            )],width="4")
                        ],justify="center", align="center",

                    ),
                    html.Br(),

                    dcc.Graph(id="comparison-graph"),
                ]),
           )], width=9),



    ], justify="center", align="center"),
])

continent_layout = html.Div([
    # Graphs
    dbc.Row(
        html.H5("Pick a continent"), justify="center", align="center",
    ),
])

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
    #dbc.Row([
    #    dbc.Button("Primary", outline=True, color="primary", className="mr-1"),
    #    dbc.Button(
    #        "Secondary", outline=True, color="primary", className="mr-1"
    #    ),
    #    dbc.Button("Success", outline=True, color="primary", className="mr-1"),
    #    dbc.Button("Warning", outline=True, color="primary", className="mr-1"),
    #    dbc.Button("Danger", outline=True, color="primary", className="mr-1"),
    #    dbc.Button("Info", outline=True, color="primary", className="mr-1"),
    #    dbc.Button("Light", outline=True, color="primary", className="mr-1"),
    #    dbc.Button("Dark", outline=True, color="primary"),
    #    
    #], justify="center", align="center",),

    dbc.Row([
        dbc.ButtonGroup([
            dbc.Button("Countries", outline=False, color="primary", id="countries", active=True),
            dbc.Button("Continents", outline=False, color="primary", id="continents")
        ]),
    ], justify="center", align="center",),

    # Space
    html.Br(),
    
    html.Div(id="country-continent-layout", children=country_layout)

])

@app.callback(
    Output('comparison-graph', "figure"),
    [
        Input("comparison-countries", "value"),
        Input("y_axis_comparison", "value"),
    ]
)
def plot_comparison(countries, y_key):

    if not isinstance(countries, list):
        countries = [countries]

    cdf = owid_covid.df

    # Filter
    cdf = cdf[cdf["location"].isin(countries)]
    # Key
    y_var = owid_covid.convert_to_original(y_key)

    #Fig
    fig = px.line(cdf, x="date", y=y_var, color="location",
                labels={
                    "date": "Time",
                    y_var:y_key,
                    "location": "Country"
                })
    return fig

@app.callback(
    [
        Output("total-deaths", "children"),
        Output("total-cases", "children"),
        Output("total-tests", "children"),
        Output("population", "children"),
        Output("pop-dens", "children"),
        Output("life-exp", "children"),
    ],
    [
        Input("focus-country", "value")
    ]
)
def display_stats(country):

    cdf = owid_covid.df[owid_covid.df["location"]==country]

    total_deaths = cdf["total_deaths"].max()
    total_cases = cdf["total_cases"].max()
    total_tests = cdf["total_tests"].max()

    total_deaths = "Total deaths: " + data_utils.human_format(total_deaths)
    total_cases = "Total cases: " + data_utils.human_format(total_cases)
    total_tests = "Total tests: " + data_utils.human_format(total_tests)

    population = cdf["population"].max()
    population = "Population: " + data_utils.human_format(population)

    popdens = cdf["population_density"].max()
    popdens = "Population density: " + str(round(popdens, 2)) + " per square km"

    lifeexp = cdf["life_expectancy"].max()
    lifeexp = "Life expectancy: " + str(round(lifeexp,2))

    return total_deaths, total_cases, total_tests, population, popdens, lifeexp

@app.callback(
    Output("country-continent-layout", "children"),
    [
        Input("countries", "active"),
        Input("continents", "active"),
    ]
)
def toggle_page(country_active, continent_active):
    layout = "404"
    if country_active:
        layout = country_layout
    elif continent_active:
        layout = continent_layout
    return layout

# this callback uses dash.callback_context to figure out which button
# was clicked most recently. it then updates the "active" style of the
# buttons appropriately, and sets some output. it could be split into
# multiple callbacks if you prefer.
@app.callback(
    [
        Output("countries", "active"),
        Output("continents", "active"),
    ],
    [
        Input("countries", "n_clicks"),
        Input("continents", "n_clicks"),
    ],
)
def toggle_buttons(n_countries, n_continents):
    ctx = dash.callback_context

    if not ctx.triggered:
        raise PreventUpdate
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if not any([n_countries, n_continents]):
        return False, False
    elif button_id=="countries":
        return True, False
    elif button_id=="continents":
        return False, True

@app.callback(
    Output('app-1-display-value', 'children'),
    [Input('app-1-dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)


@app.callback(
        Output("collapse", "is_open"),
        Output("collapse2", "is_open"),
    [
        Input("focus-country", "value"),
    ],
    [
        State("collapse", "is_open"),
        State("collapse2", "is_open"),
    ],
)
def toggle_restrictions(country, is_open, is_open2):
    iso = owid_covid.convert_cname_iso(country)

    cdf = oxcgrt.df
    is_open=False
    is_open2=False
    if cdf["CountryCode"].str.contains(iso).any():
        is_open=True
        is_open2=True
    
    return is_open, is_open2

@app.callback(
    Output("y_axis_c", "options"),
    [
        Input("focus-country", "value"),
    ]
)
def update_y_dropdown(country):
    cdf = owid_covid.df[owid_covid.df["location"]==country]

    # Only display data with less than 70% NaN
    valid_data = cdf.columns[cdf.isnull().sum()/len(cdf) < .7]
    pos_data = owid_covid.y_axis_labels

    labels = []

    for i in range(len(valid_data)):
        if valid_data[i] in (pos_data):
            labels.append(valid_data[i])

    options=[{'label': i, 'value': i} for i in owid_covid.convert_to_readable(labels)]

    return options

@app.callback(
    Output("graph_info4", "children"),
    [
        Input("restriction", "value"),
    ]
)
def update_info4(restriction):
    l = html.H5("")
    if restriction != "None":
        k = oxcgrt.get_oxcgrt_key(restriction)
        descriptions = oxcgrt.coding[k]
        
        if descriptions[4] != "NaN":
            l = dbc.Row([
                html.P("Level 4: "),
                html.P(descriptions[4])
                ], align="center", justify="center"),
    return l

@app.callback(
    Output("graph_info3", "children"),
    [
        Input("restriction", "value"),
    ]
)
def update_info3(restriction):
    l = html.H5("")
    if restriction != "None":
        k = oxcgrt.get_oxcgrt_key(restriction)
        descriptions = oxcgrt.coding[k]
        l = html.H5("")
        if descriptions[3] != "NaN":
            l = dbc.Row([
                html.P("Level 3: "),
                html.P(descriptions[3])
                ], align="center", justify="center"),
    return l

@app.callback(
    Output("graph_info2", "children"),
    [
        Input("restriction", "value"),
    ]
)
def update_info2(restriction):
    print("hello")
    l = html.H5("")
    if restriction != "None":
        print("before 2")
        k = oxcgrt.get_oxcgrt_key(restriction)
        descriptions = oxcgrt.coding[k]
        if descriptions[2] != "NaN":
            print("after 2")
            l = dbc.Row([
                html.P("Level 2: "),
                html.P(descriptions[2])
                ], align="center", justify="center"),
    return l


@app.callback(
    [
    Output("country_graph", "figure"),
    Output("graph_info", "children"),
    ],
    [
        Input("focus-country", "value"),
        Input("restriction", "value"),
        Input("y_axis_c", "value"),
    ]
)
def plot_graph(country, restriction, y_key):
    cdf = owid_covid.df[owid_covid.df["location"]==country]
    y_axis = owid_covid.convert_to_original(y_key)
    
    fig = px.line(x=cdf["date"], y=cdf[y_axis])

    fig.update_layout(
        xaxis_title="Time",
        yaxis_title=y_key
    )

    # Convert to alpha3 code
    iso_code = owid_covid.convert_cname_iso(country)

    lay = html.H5("")

    if restriction != "None":
        step = 0
        cdf = oxcgrt.df[oxcgrt.df["CountryCode"]==iso_code]
        cdf = cdf.set_index(cdf["Date"])

        cdf = cdf[cdf["Jurisdiction"]=="NAT_TOTAL"]
        si = cdf[oxcgrt.get_oxcgrt_key(restriction)].dropna()

        colors = px.colors.sequential.Plasma[::2]

        for i in range(1, round(si.max()+1)):
        

            test = si[si==i]
            test = pd.DataFrame(test)
            test["identifier"] = (~test.index.to_series().diff().dt.days.div(1, fill_value=0).lt(2)).cumsum()

            for i,grp in test.groupby('identifier'):
                if len(grp)>=4:
                    step+=1
                    grp = grp.sort_index()
                    value = grp[oxcgrt.get_oxcgrt_key(restriction)][0]
                    fig.add_vrect(x0=grp.index.min(), x1=grp.index.max(), 
                                fillcolor=colors[int(value)-1], opacity=0.25, line_width=1)
                    fig.add_shape(type='line',
                            x0=grp.index.mean(),
                            y0=0.99,
                            x1=grp.index.mean(),
                            y1=1,
                            line=dict(color='black', dash='dot'),
                            xref='x',
                            yref='paper'
                    )

                    fig.add_annotation(dict(font=dict(color="black",size=12),
                                        #x=x_loc,
                                        x=grp.index.mean(),
                                        y=1.06,
                                        showarrow=False,
                                        text='<b>'+ ("L: " + str(int(value))) +'</b>',
                                        textangle=0,
                                        xref="x",
                                        yref="paper"
                                    ))

        k = oxcgrt.get_oxcgrt_key(restriction)
        descriptions = oxcgrt.coding[k]
        layo=[]
        #for i in range(len(descriptions)):
        l = dbc.Row([
            html.P("Level 1: "),
            html.P(descriptions[1])
            ], align="center", justify="center"),

        #    layo = layo + [l]

        lay = l   
        
    return fig, lay

@app.callback(
    Output("total_cases", "figure"),
    [Input("focus-country", "value")]
)
def plot_total_deaths(country):
    cdf = owid_covid.df[owid_covid.df["location"]==country]
    fig = px.line(x=cdf["date"], y=cdf["total_cases"])
    return fig

@app.callback(
    [
    Output("current-country", "children"),
    Output("restriction", "value"),
    ],
    [Input("focus-country", "value")]
)
def get_current_country(country):
    return country, "None"

@app.callback(
    Output("current-country-image", "src"),
    [Input("focus-country", "value")]
)
def get_country_image(country):
    cdf = owid_covid.df[owid_covid.df["location"]==country]
    iso = cdf["iso_code"].unique()
    a2 = pycountry.countries.get(alpha_3=iso[0])
    src = "https://www.countryflags.io/" + str(a2.alpha_2) + "/flat/64.png"
    return src