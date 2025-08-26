import dash_bootstrap_components as dbc
from wordcloud import WordCloud
from dash import html, dcc
import duckdb
import base64
from queries.queries import temp_table, word_query, bar_query
import plotly.express as px
from io import BytesIO
from dash_bootstrap_templates import load_figure_template

con = duckdb.connect()
con.execute(temp_table)

load_figure_template()


def word_cloud_plot(worddf):
    word_dict = dict(zip(worddf["Word"], worddf["Count"]))
    wordcloud = WordCloud(
        width=1200,
        height=590,
        background_color=None,
        mode="RGBA",
        colormap="YlOrRd",
    ).generate_from_frequencies(word_dict)
    return wordcloud


def word_cloud_func(borough, year_range):
    start_year, end_year = year_range

    if not borough:
        borough = ["QUEENS", "BROOKLYN", "MANHATTAN", "BRONX", "STATEN ISLAND"]

    params = (borough, start_year, end_year)

    worddf = con.execute(word_query, parameters=params).df()
    wordcloud = word_cloud_plot(worddf)
    buffer = BytesIO()
    wordcloud.to_image().save(buffer, format="PNG")
    img_base64 = base64.b64encode(buffer.getvalue()).decode()

    return f"data:image/png;base64,{img_base64}"


def bar_plot(borough, year_range, template):
    start_year, end_year = year_range

    if not borough:
        borough = ["QUEENS", "BROOKLYN", "MANHATTAN", "BRONX", "STATEN ISLAND"]

    params = (borough, start_year, end_year)
    dfb = con.execute(bar_query, parameters=params).df()
    dfb["Vehicle"] = dfb["Vehicle"].str.title()

    fig_bar = px.bar(
        dfb,
        x="Vehicle",
        y="counts",
        color="Vehicle",
        orientation="v",
        title="Top vehicle types in collisions",
        text_auto=".2s",
        color_discrete_sequence=px.colors.qualitative.Set1,
        template=template,
    ).update_layout(
        showlegend=False,
        autosize=True,
        margin=dict(t=80, r=10, b=20, l=10),
        yaxis=dict(title="Number of Collisions"),
    )
    return fig_bar


def word_bar(borough, year_range, template):
    return dbc.Card(
        dbc.CardBody(
            dbc.Row(
                [
                    dbc.Col(
                        children=[
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.H6(
                                            "Top Contributing Factors",
                                            className="mb-3",
                                        ),
                                        html.Img(
                                            src=word_cloud_func(borough, year_range),
                                            style={"width": "100%", "height": "auto"},
                                        ),
                                    ]
                                ),
                                style={"borderColor": "rgba(0,0,0,0.3)"},
                            )
                        ],
                        xs=12,
                        md=6,
                        className="mb-3 mb-md-0",
                    ),
                    dbc.Col(
                        children=[
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        dcc.Graph(
                                            figure=bar_plot(
                                                borough, year_range, template
                                            ),
                                            config={
                                                "displayModeBar": False,
                                                "staticPlot": True,
                                            },
                                            style={"height": "100%"},
                                        ),
                                    ]
                                ),
                                style={"borderColor": "rgba(0,0,0,0.3)"},
                            )
                        ],
                        xs=12,
                        md=6,
                    ),
                ],
            ),
        ),
        className="mt-3 shadow-sm",
    )
