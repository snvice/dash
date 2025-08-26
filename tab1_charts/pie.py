import dash_bootstrap_components as dbc
from dash import dcc
import duckdb
from queries.queries import temp_table, pie_query, line_query
import plotly.express as px
from dash_bootstrap_templates import load_figure_template

con = duckdb.connect()
con.execute(temp_table)

load_figure_template()


def pie_chart(borough, year_range, template):
    start_year, end_year = year_range

    if not borough:
        borough = ["QUEENS", "BROOKLYN", "MANHATTAN", "BRONX", "STATEN ISLAND"]

    params = (borough, start_year, end_year)
    piedf = con.execute(pie_query, parameters=params).df()
    piedf = piedf[piedf["vehicle_count"] > 0]
    labels = {1: "1 Car", 2: "2 Cars", 3: "3 Cars"}
    piedf["vehicle_label"] = piedf["vehicle_count"].map(labels)

    pull_values = [0.02, 0.03, 0.03]

    return (
        px.pie(
            piedf,
            names="vehicle_label",
            values="crashes",
            color_discrete_sequence=px.colors.qualitative.Set1,
            title="Distribution of crashes by number of vehicles involved",
            template=template,
        )
        .update_traces(
            textinfo="percent+label",
            textposition="inside",
            textfont_size=16,
            # hole=0.2,
            pull=pull_values,
        )
        .update_layout(
            showlegend=False,
            margin=dict(t=50, b=0, l=10, r=0),
            yaxis=dict(title="Number of Collisions"),
        )
    )


def line_chart(borough, year_range, template):
    start_year, end_year = year_range

    if not borough:
        borough = ["QUEENS", "BROOKLYN", "MANHATTAN", "BRONX", "STATEN ISLAND"]

    params = (borough, start_year, end_year)
    linedf = con.execute(line_query, parameters=params).df()

    fig = px.line(
        linedf,
        x="Year",
        y="total_collisions",
        color="BOROUGH",
        title="Collisions per Year",
        markers=True,
        template=template,
        color_discrete_sequence=px.colors.qualitative.Set1,
        line_shape="spline",
        category_orders={
            "BOROUGH": ["BROOKLYN", "QUEENS", "MANHATTAN", "BRONX", "STATEN ISLAND"]
        },
        range_x=[2018, 2026],
    ).update_layout(
        margin=dict(t=50, b=0, l=10, r=10),
        yaxis=dict(title="Number of Collisions"),
        legend=dict(orientation="h", y=0.9, yanchor="bottom", x=0.6, xanchor="center"), 
        legend_title=None,
    )

    return fig


def pie(borough, year_range, template):
    return dbc.Card(
        dbc.CardBody(
            dbc.Row(
                [
                    dbc.Col(
                        children=[
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        dcc.Graph(
                                            figure=pie_chart(
                                                borough, year_range, template
                                            ),
                                            config={
                                                "displayModeBar": False,
                                                "staticPlot": True,
                                            },
                                            style={"height": "450px", "width": "100%"},
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
                                            figure=line_chart(
                                                borough, year_range, template
                                            ),
                                            config={
                                                "displayModeBar": False,
                                                "staticPlot": True,
                                            },
                                            style={"height": "450px", "width": "100%"},
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


# remember to change from parquet to crashes
