import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from data import (
    countries_df,
    totals_df,
    dropdown_options,
    make_global_df,
    make_country_df,
)
from builders import make_table
from dash.dependencies import Input, Output

stylesheets = [
    "https://cdn.jsdelivr.net/npm/reset-css@5.0.1/reset.min.css",
    "https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600&display=swap",
]

app = dash.Dash(__name__, external_stylesheets=stylesheets)

app.title = "Rona Dashboard"

# expose the server for heroku
server = app.server

bubble_map = px.scatter_geo(
    countries_df,
    size="Confirmed",
    hover_name="Country_Region",
    color="Confirmed",
    locations="Country_Region",
    locationmode="country names",
    size_max=40,
    title="Confirmed By Country",
    template="plotly_dark",
    color_continuous_scale=px.colors.sequential.Oryel,
    projection="orthographic",
    hover_data={
        "Confirmed": ":,",
        "Deaths": ":,",
        "Recovered": ":,",
        "Country_Region": False,
    },
)

bubble_map.update_layout(
    margin=dict(l=0, r=0, t=50, b=0), coloraxis_colorbar=dict(xanchor="left", x=0)
)


bars_graph = px.bar(
    totals_df,
    x="condition",
    hover_data={"count": ":,"},
    y="count",
    template="plotly_dark",
    title="Total Global Cases",
    labels={"condition": "Condition", "count": "Count", "color": "Condition"},
)

# bars_graph.update_layout(xaxis=dict(title="Condition"), yaxis=dict(title="Count"))
bars_graph.update_traces(marker_color=["#e74c3c", "#8e44ad", "#27ae60"])

app.layout = html.Div(
    style={
        "textAlign": "center",
        "minHeight": "100vh",
        "backgroundColor": "#111111",
        "color": "white",
    },
    children=[
        html.Header(
            style={"textAlign": "center", "paddingTop": "50px", "marginBottom": 100},
            children=[html.H1("Corona Dashboard", style={"fontSize": 40})],
        ),
        html.Div(
            style={
                "display": "grid",
                "gap": 50,
                "gridTemplateColumns": "repeat(4, 1fr)",
            },
            children=[
                # html.Div(children=[dcc.Graph(figure=bubble_map)]),
                html.Div(
                    style={"grid-column": "span 3"},
                    children=[dcc.Graph(figure=bubble_map)],
                ),
                html.Div(children=[make_table(countries_df)]),
            ],
        ),
        html.Div(
            style={
                "display": "grid",
                "gap": 50,
                "gridTemplateColumns": "repeat(4, 1fr)",
            },
            children=[
                html.Div(children=[dcc.Graph(figure=bars_graph)]),
                html.Div(
                    style={"grid-column": "span 3"},
                    children=[
                        dcc.Dropdown(
                            style={
                                "width": 320,
                                "margin": "0 auto",
                                "color": "black",
                            },
                            placeholder="Select a Country",
                            id="country",
                            options=[
                                {"label": country, "value": country}
                                for country in dropdown_options
                            ],
                        ),
                        dcc.Graph(id="country_graph"),
                    ],
                ),
            ],
        ),
    ],
)


@app.callback(Output("country_graph", "figure"), [Input("country", "value")])
def update_hello(value):
    if value:
        df = make_country_df(value)
    else:
        df = make_global_df()
    fig = px.line(
        df,
        x="index",
        y=["confirmed", "deaths", "recovered"],
        template="plotly_dark",
        labels={"value": "Cases", "variable": "Condition", "index": "Date"},
        hover_data={"value": ":,", "variable": False, "index": False},
        color_discrete_map={
            "confirmed": "#e74c3c",
            "deaths": "#8e44ad",
            "recovered": "#27ae60",
        },
    )
    fig.update_xaxes(rangeslider_visible=True)
    # fig["data"][0]["line"]["color"] = "#e74c3c"
    # fig["data"][1]["line"]["color"] = "#8e44ad"
    # fig["data"][2]["line"]["color"] = "#27ae60"
    return fig
