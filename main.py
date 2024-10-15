import dash
import dash_mantine_components as dmc
import numpy as np
import pandas as pd
import plotly.express as px
from dash import Input, Output, State, dcc, html

country = [
    "Global",
    "Afghanistan",
    "Angola",
    "Albania",
    "United Arab Emirates",
    "Armenia",
    "Azerbaijan",
    "Burundi",
    "Benin",
    "Burkina Faso",
    "Bangladesh",
    "Bahrain",
    "Bahamas",
]
app = dash.Dash(
    __name__, external_stylesheets=["https://unpkg.com/@mantine/dates@7/styles.css"]
)
h = 300
df_stroke = pd.read_csv("brain_stroke.csv")
df_testing = pd.read_csv("HIV_ANC_Testing_2023.csv")
df_children = pd.read_csv("HIV_Children_2023.csv")
df_infant = pd.read_csv("HIV_Early_Infant_Diagnosis_2023.csv")
df_paediatric = pd.read_csv("HIV_Paediatric_2023.csv")
df_pmtct = pd.read_csv("HIV_PMTCT_2023.csv")
df_inc_2022 = pd.read_csv("dataset-asr-inc-both-sexes-in-2022-all-cancers.csv")
df_mort_2022 = pd.read_csv("dataset-asr-mort-both-sexes-in-2022-all-cancers.csv")
df_abs = pd.read_csv(
    "dataset-absolute-numbers-inc-males-and-females-age-0-84-1943-2018-all-sites-excl-non-melanoma-skin-cancer.csv"
)

app.layout = html.Div(
    [
        html.Div(
            [
                html.Button(
                    "para",
                    id="button",
                ),
                html.Div(
                    html.H1("World Deadly Diseases Analysis"),
                    style={"display": "inline-block"},
                ),
            ]
        ),
        dmc.Drawer(
            id="drawer",
            title="parameters",
            zIndex=1000,
            children=[
                dmc.Select(
                    id="disease",
                    label="Select the disease",
                    data=[
                        {"value": "AIDS", "label": "AIDS"},
                        {"value": "Stroke", "label": "Stroke"},
                        {"value": "Cancer", "label": "Cancer"},
                    ],
                    value="AIDS",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                dmc.Select(
                                    id="year",
                                    label="Year",
                                    data=[
                                        {"value": 2015, "label": 2015},
                                        {"value": 2017, "label": 2017},
                                        {"value": 2018, "label": 2018},
                                        {"value": 2019, "label": 2019},
                                        {"value": 2020, "label": 2020},
                                        {"value": 2021, "label": 2021},
                                        {"value": 2022, "label": 2022},
                                    ],
                                    value=2022,
                                ),
                                dmc.Select(
                                    id="p/n",
                                    label="percent/number",
                                    data=[
                                        {"value": "p", "label": "percent"},
                                        {"value": "n", "label": "number"},
                                    ],
                                    value="p",
                                ),
                                dmc.Select(
                                    id="country",
                                    label="Country",
                                    data=[{"value": c, "label": c} for c in country],
                                    value="Global",
                                ),
                            ],
                            id="AIDS_para",
                            style={"position": "fixed", "top": "120px", "left": "5px"},
                        ),
                        html.Div(
                            [
                                dmc.Select(
                                    id="bar_variable",
                                    label="Select the for bar graph",
                                    data=[
                                        {"value": c, "label": c}
                                        for c in df_stroke.columns
                                    ],
                                    value="gender",
                                ),
                                dmc.Select(
                                    id="hist_variable",
                                    label="Select the for histogram",
                                    data=[
                                        {"value": c, "label": c}
                                        for c in df_stroke.columns
                                    ],
                                    value="age",
                                ),
                            ],
                            id="stroke_para",
                            style={"position": "fixed", "top": "120px", "left": "5px"},
                        ),
                        html.Div(
                            "Cancer",
                            id="cancer_para",
                            style={"position": "fixed", "top": "120px", "left": "5px"},
                        ),
                    ]
                ),
            ],
        ),
        dcc.Graph(
            id="graph1",
            style={"width": "50%", "display": "inline-block"},
        ),
        dcc.Graph(
            id="graph2",
            style={"width": "50%", "display": "inline-block"},
        ),
        dcc.Graph(
            id="graph3",
            style={"width": "33%", "display": "inline-block"},
        ),
        dcc.Graph(
            id="graph4",
            style={"width": "34%", "display": "inline-block"},
        ),
        dcc.Graph(
            id="graph5",
            style={"width": "33%", "display": "inline-block"},
        ),
    ],
)


@app.callback(
    Output("drawer", "opened"),
    Input("button", "n_clicks"),
    prevent_initial_call=True,
)
def toggle_drawer(n_clicks):
    return n_clicks > 0


@app.callback(
    [
        Output("AIDS_para", "style"),
        Output("stroke_para", "style"),
        Output("cancer_para", "style"),
    ],
    Input("disease", "value"),
    [
        State("AIDS_para", "style"),
        State("stroke_para", "style"),
        State("cancer_para", "style"),
    ],
)
def update_para(value, AIDS_para, stroke_para, cancer_para):
    if value == "AIDS":
        stroke_para["visibility"] = "hidden"
        cancer_para["visibility"] = "hidden"
        AIDS_para["visibility"] = "visible"
    elif value == "Stroke":
        AIDS_para["visibility"] = "hidden"
        cancer_para["visibility"] = "hidden"
        stroke_para["visibility"] = "visible"
    elif value == "Cancer":
        AIDS_para["visibility"] = "hidden"
        stroke_para["visibility"] = "hidden"
        cancer_para["visibility"] = "visible"
    return AIDS_para, stroke_para, cancer_para


@app.callback(
    [
        Output("graph1", "figure"),
        Output("graph2", "figure"),
        Output("graph3", "figure"),
        Output("graph4", "figure"),
        Output("graph5", "figure"),
    ],
    [
        Input("disease", "value"),
        Input("year", "value"),
        Input("p/n", "value"),
        Input("country", "value"),
        Input("bar_variable", "value"),
        Input("hist_variable", "value"),
    ],
)
def update_graph(disease, year, p_n, country, bar_variable, hist_variable):
    if disease == "AIDS":
        if p_n == "n":
            indicator = "Number of pregnant women presenting at ANC who were tested for HIV or already knew their HIV positive status"
        else:
            indicator = "Per cent of pregnant women presenting at ANC who were tested for HIV or already knew their HIV positive status"
        df_ = df_testing[(df_testing["Indicator"] == indicator)]
        df_ = df_[df_["Year"] == year]
        fig1 = px.choropleth(
            df_,
            locations="ISO3",
            color="Value",
            height=h,
            title="women presenting at ANC who were tested for HIV",
        )

        if p_n == "n":
            indicator = "Reported number of infants born to pregnant women living with HIV who received a virological test for HIV within 2 months of birth"
        else:
            indicator = "Per cent of infants born to pregnant women living with HIV who received a virological test for HIV within 2 months of birth"
        df_ = df_infant[(df_infant["Indicator"] == indicator)]
        df_ = df_[df_["Year"] == year]
        fig2 = px.choropleth(
            df_,
            locations="ISO3",
            color="Value",
            height=h,
            title="infants born to pregnant women living with HIV",
        )

        if p_n == "n":
            indicator = "Reported number of children receiving ART"
        else:
            indicator = "Per cent of children living with HIV receiving ART"

        df_ = df_paediatric[df_paediatric["Country/Region"] == country]
        df_ = df_[df_["Indicator"] == indicator]
        fig3 = px.line(
            df_,
            x="Year",
            y=["Value", "Lower", "Upper"],
            height=h,
            title=f"children receiving ART at {country}",
        )

        if p_n == "n":
            indicator = "Reported number of pregnant women living with HIV receiving lifelong ART"
        else:
            indicator = (
                "Per cent of pregnant women living with HIV receiving lifelong ART"
            )

        df_ = df_pmtct[df_pmtct["Country/Region"] == country]
        df_ = df_[df_["Indicator"] == indicator]
        fig4 = px.line(
            df_,
            x="Year",
            y=["Value", "Lower", "Upper"],
            height=h,
            title=f"women with HIV receiving lifelong ART at {country}",
        )

        indicator = "Estimated incidence rate (new HIV infection per 1,000 uninfected population)"
        df_ = df_children[df_children["Country/Region"] == country]
        df_ = df_[df_["Indicator"] == indicator]
        df_ = df_[df_["Sex"] == "Both"]
        df_ = df_[df_["Age"] == "Age 0-14"]
        fig5 = px.line(
            df_,
            x="Year",
            y=["Value", "Lower", "Upper"],
            height=h,
            title=f"Estimated incidence rate (per 1,000) at {country}",
        )
    elif disease == "Stroke":
        varValue = df_stroke[bar_variable].value_counts()
        fig1 = px.bar(
            varValue,
            x=varValue.index,
            y=varValue,
            title=f"{bar_variable} Frequency",
            height=h,
            color=varValue.index,
        )
        fig1.update_layout(
            xaxis_title=bar_variable,
            yaxis_title="Frequency",
            legend_title="Legend",
        )
        fig2 = px.histogram(
            df_stroke, x=hist_variable, height=h, title=f"{hist_variable} Distribution"
        )
        fig3 = px.violin(
            df_stroke,
            x="gender",
            y="age",
            box=True,
            points="all",
            height=h,
            color="gender",
            title="Age and Gender Distribution",
        )
        fig4 = px.violin(
            df_stroke,
            y="avg_glucose_level",
            x="smoking_status",
            box=True,
            points="all",
            height=h,
            color="smoking_status",
            title="Glucose Level and Smoking Status Distribution",
        )
        fig5 = px.violin(
            df_stroke,
            y="bmi",
            x="smoking_status",
            box=True,
            points="all",
            height=h,
            color="smoking_status",
            title="BMI and Smoking Status Distribution",
        )
    elif disease == "Cancer":
        fig1 = px.choropleth(
            df_inc_2022,
            locations="Alpha‑3 code",
            color="ASR (World) per 100 000",
            height=h,
            title="Incedence Rate (World) per 100 000",
        )
        fig2 = px.choropleth(
            df_mort_2022,
            locations="Alpha‑3 code",
            color="ASR (World) per 100 000",
            height=h,
            title="Mortality Rate (World) per 100 000",
        )
        fig3 = px.line(
            df_abs,
            x="Year",
            y="ASR (World)",
            color="Sex",
            height=h,
            title="Gender comparison of HIV Incedence Rate",
        )
        fig4 = px.line(
            df_abs,
            x="Year",
            y="Crude rate",
            color="Sex",
            height=h,
            title="Gender comparison of HIV Crude Rate",
        )
        fig5 = px.line(
            df_abs,
            x="Year",
            y="Total",
            color="Sex",
            height=h,
            title="Gender comparison of HIV incidence and mortality",
        )
    return fig1, fig2, fig3, fig4, fig5


# @app.callback(
#     [Output("graph1", "figure"), Output("graph2", "figure")],
#     [Input("year", "value"), Input("p/n", "value")],
#     prevent_initial_call=True,
#     allow_duplication=True,
# )
# def update_aids_graph1(year, p_n):
#     df_ = df_testing[
#         (
#             df_testing["Indicator"]
#             == "Number of pregnant women presenting at ANC who were tested for HIV or already knew their HIV positive status"
#             if p_n == "n"
#             else "Per cent of pregnant women presenting at ANC who were tested for HIV or already knew their HIV positive status"
#         )
#     ]
#     df_ = df_[df_["Year"] == year]
#     fig1 = px.choropleth(df_, locations="ISO3", color="Value", height=h)
#     df_ = df_infant[
#         (
#             df_infant["Indicator"]
#             == "Reported number of infants born to pregnant women living with HIV who received a virological test for HIV within 2 months of birth"
#             if p_n == "n"
#             else "Per cent of infants born to pregnant women living with HIV who received a virological test for HIV within 2 months of birth"
#         )
#     ]
#     df_ = df_[df_["Year"] == year]
#     fig2 = px.choropleth(df_, locations="ISO3", color="Value", height=h)
#     return fig1, fig2


if __name__ == "__main__":
    app.run_server(debug=True)
