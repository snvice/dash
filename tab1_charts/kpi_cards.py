from dash import html
import dash_bootstrap_components as dbc
import duckdb
from queries.queries import temp_table, kpi_query

icons = "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css"

con = duckdb.connect()
con.execute(temp_table)


def kpi_cards(borough, year_range):
    start_year, end_year = year_range

    if not borough:
        borough = ["QUEENS", "BROOKLYN", "MANHATTAN", "BRONX", "STATEN ISLAND"]

    params = (borough, start_year, end_year)

    total_collisions, persons_killed, persons_injured = map(
        int, con.execute(kpi_query, parameters=params).fetchone()
    )

    return dbc.Row(
        [
            dbc.Col(
                [
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.Small(
                                    [
                                        html.I(
                                            className="fa-solid fa-car-burst me-2",
                                            style={"fontSize": "24px"},
                                        ),
                                        "Total Collisions",
                                    ]
                                ),
                                html.H4(f"{total_collisions:,}"),
                            ]
                        ),
                        className="mt-3 text-center",
                        outline=True,
                        color="secondary",
                    )
                ],
                width="auto",
                xs=4,
                md=2,
            ),
            dbc.Col(
                [
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.Small(
                                    [
                                        html.I(
                                            className="fa-solid fa-user-injured me-2",
                                            style={"fontSize": "24px"},
                                        ),
                                        "Persons Injured",
                                    ]
                                ),
                                html.H4(f"{persons_injured:,}"),
                            ]
                        ),
                        className="mt-3 text-center",
                        outline=True,
                        color="warning",
                    )
                ],
                width="auto",
                xs=4,
                md=2,
            ),
            dbc.Col(
                [
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.Small(
                                    [
                                        html.I(
                                            className="fa-solid fa-shoe-prints me-2",
                                            style={"fontSize": "24px"},
                                        ),
                                        "Persons Killed",
                                    ]
                                ),
                                html.H4(f"{persons_killed:,}"),
                            ]
                        ),
                        className="mt-3 text-center",
                        outline=True,
                        color="danger",
                    )
                ],
                width="auto",
                xs=4,
                md=2,
            ),
        ],
        justify="center",
    )
