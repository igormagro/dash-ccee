# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import requests as req
import json

res = json.loads(req.get("https://ccee-template-data.s3.amazonaws.com/contracts.json").content)

df = pd.DataFrame(res)[["date","companyName","MWavg","type"]].groupby(["date","companyName","type"]).sum().reset_index()
companies = sorted(list(df.companyName.unique()))


app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.Div([
        html.Div([
            html.H2("Dash example: CCEE energy contracts", className="header__title")
        ], id="header"),

    dcc.Dropdown(placeholder="Select a company", id="company-selector", options=[{"value":x, "label":x} for x in companies]),
        html.Div(id="test")
    ], id="page-content"),
    html.Div([
        html.P("Made with 🧠 by Igor Magro")
    ],id="footer")
])

@app.callback(
    Output("test","children"),
    Input("company-selector","value"),
)
def loadChart(company):
    filtered_df = df.query(f"companyName == '{company}'")
    sell = filtered_df.query(f"type == 'sell'")
    buy = filtered_df.query(f"type == 'buy'")
    fig = go.Figure()
    fig.add_trace( go.Scatter(x=sell.date, y=sell.MWavg, name="sell",line_shape="spline"))
    fig.add_trace( go.Scatter(x=buy.date, y=buy.MWavg, name="buy",line_shape="spline"))

    return dcc.Graph(figure=fig)


    

if __name__ == '__main__':
    app.run_server()