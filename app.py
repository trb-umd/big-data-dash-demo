import data_prep

import dash
from dash import dcc
from dash import html
import pandas as pd


def load_files():
    print("\nAttempting to load processed CSV files...")

    gender_death = pd.read_csv("./csv/gender_death.csv")
    age_death = pd.read_csv("./csv/age_death.csv")
    province_deaths = pd.read_csv("./csv/province_deaths.csv")
    financing_source = pd.read_csv("./csv/financing_source.csv")
    week_deaths = pd.read_csv("./csv/week_deaths.csv")

    print("Success.")

    return gender_death, age_death, financing_source, province_deaths, week_deaths

# attempt to load pre-processed CSV files for speed

try:
    gender_death, age_death, financing_source, province_deaths, week_deaths = load_files()

except:

    print("\nProcessed CSV files not found, creating...\n")
    data_prep.prep_data()
    gender_death, age_death, financing_source, province_deaths, week_deaths = load_files()

app = dash.Dash(__name__)

# Dashboard layout - templates/themes not utilized to demonstrate that each component can be modified as desired.
# Here, a custom dark theme was utilized throughout

app.layout = html.Div(
    style={'backgroundColor': "rgb(10,10,10)"},
    children=[
        html.H1(children="COVID-19 in Argentina", style={"textAlign": "center",
            "backgroundColor": "rgb(10,10,10)",
            "color": "rgb(255,255,255)",
            }
        ),
        html.P(children="Metrics from 01/01/2020 to 08/07/2021", style={
            "textAlign": "center",
            "backgroundColor": "rgb(10,10,10)",
            "color": "rgb(255,255,255)",
            }
       ),
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": gender_death["patient_gender"],
                        "y": gender_death["patient_death"],
                        "type": "bar",
                    },
                ],
                 "layout": {
                    "title": "Deaths by Patient Gender",
                    "xaxis": {"title": "Patient Gender"},
                    "yaxis": {"title": "Patient Deaths"},
                    "template": "plotly_dark",
                    "font": {"size": 16, "color": "rgb(255,255,255"},
                    "paper_bgcolor": "rgb(10,10,10)",
                    "plot_bgcolor": "rgb(17,17,17)",
                },
            },
        ),
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": age_death["patient_age"],
                        "y": age_death["patient_death"],
                        "type": "line"
                     },
                ],
                 "layout": {
                    "title": "Covid Deaths by Age",
                    "xaxis": {"title": "Patient Age"},
                    "yaxis": {"title": "Patient Deaths"},
                    "font": {"size": 16, "color": "rgb(255,255,255"},
                    "paper_bgcolor": "rgb(10,10,10)",
                    "plot_bgcolor": "rgb(17,17,17)",
                },
            },
        ),
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": financing_source["financing_source"],
                        "y": financing_source["patient_death"],
                        "type": "bar"
                    },
                ],
                "layout": {
                    "title": "Publicly vs Privately Funded Care Deaths",
                    "xaxis": {"title": "Financing Source"},
                    "yaxis": {"title": "Patient Deaths"},
                    "font": {"size": 16, "color": "rgb(255,255,255"},
                    "paper_bgcolor": "rgb(10,10,10)",
                    "plot_bgcolor": "rgb(17,17,17)",
                },
            },
        ),
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": province_deaths["residence_province"],
                        "y": province_deaths["patient_death"],
                        "type": "bar"
                    },
                ],
                 "layout": {
                    "title": "Deaths by Residence Province",
                    "xaxis": {"title": "Province of Origin"},
                    "yaxis": {"title": "Patient Deaths"},
                    "font": {"size": 16, "color": "rgb(255,255,255"},
                    "paper_bgcolor": "rgb(10,10,10)",
                    "plot_bgcolor": "rgb(17,17,17)",
                },
            },
        ),
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": week_deaths["pandemic_week"],
                        "y": week_deaths["patient_death"],
                        "type": "line"
                    },
                ],
                 "layout": {
                    "title": "Deaths per Week of Pandemic",
                    "xaxis": {"title": "Pandemic Week"},
                    "yaxis": {"title": "Patient Deaths"},
                    "font": {"size": 16, "color": "rgb(255,255,255"},
                    "paper_bgcolor": "rgb(10,10,10)",
                    "plot_bgcolor": "rgb(17,17,17)",
                },
            },
        ),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
