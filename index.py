# Import Dash dependencies
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Import bootstrap components
import dash_bootstrap_components as dbc


# Import pages/apps
from app import app
from apps import home
from apps import app2

server = app.server

app.layout = html.Div([
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Home", href="/")),
            dbc.NavItem(dbc.NavLink("Analysis Tool", href="/covid-tool")),
        ],
        brand="Data Analysis",
        brand_href="/",
        color="3",
        dark=False,
    ),
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    print("pathname: ", pathname)
    if pathname == '/' or pathname == "/index":
        return home.layout
    elif pathname == '/covid-tool':
        return app2.layout
    else:
        print("404")
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)