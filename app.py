import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

import pandas as pd
import requests

# Import datasets
owd_covid_url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
owd_covid_data = pd.read_csv(owd_covid_url)


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

top_markdown_text = "Hei"

nor = owd_covid_data[owd_covid_data["iso_code"].isin(["NOR", "SWE"])]

fig = px.line(nor, x="date", y="total_cases", color="iso_code")
fig.update_layout(clickmode="event+select")
fig.update_traces(marker_size=20)

app.layout = html.Div([

    dcc.Markdown(children=top_markdown_text),
    dcc.Graph(figure=fig),

])

if __name__ == '__main__':
    app.run_server(debug=True)







