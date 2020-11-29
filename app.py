# Import Dash dependencies
import dash

# Import bootstrap components
import dash_bootstrap_components as dbc

app = dash.Dash(__name__,suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.LITERA])
