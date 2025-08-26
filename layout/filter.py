from dash import html, dcc
import dash_bootstrap_components as dbc


def filters():
    return dbc.Card(
        dbc.CardBody(
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Div(
                                [
                                    html.I(
                                        className="fa-solid fa-filter me-2",
                                        style={"color": "#FFC107"},
                                    ),
                                    html.Small(
                                        "Filter by Borough",
                                        className="fw-bold",
                                    ),
                                ],
                                className="mb-2",
                            ),
                            dbc.Checklist(
                                id="borough-checklist",
                                options=[
                                    {"label": b, "value": b.upper()}
                                    for b in [
                                        "Queens",
                                        "Brooklyn",
                                        "Manhattan",
                                        "Bronx",
                                        "Staten Island",
                                    ]
                                ],
                                value=[
                                    "QUEENS",
                                    "BROOKLYN",
                                    "MANHATTAN",
                                    "BRONX",
                                    "STATEN ISLAND",
                                ],
                                inline=True,
                                switch=True,
                            ),
                        ],
                        xs=12,
                        md=6,
                        className="mb-3 mb-md-0",
                    ),
                    dbc.Col(
                        [
                            html.Div(
                                [
                                    html.I(
                                        className="fa-solid fa-filter me-2",
                                        style={"color": "#FFC107"},
                                    ),
                                    html.Small("Filter by Year", className="fw-bold"),
                                ],
                                className="mb-2",
                            ),
                            dcc.RangeSlider(
                                id="year-range",
                                min=2018,
                                max=2026,
                                step=1,
                                value=[2018, 2026],
                                marks={year: str(year) for year in range(2018, 2027)},
                                tooltip={
                                    "placement": "bottom",
                                    "always_visible": True,
                                    "style": {"color": "white"},
                                },
                                allowCross=False,
                                updatemode="mouseup",
                                pushable=1,
                                included=True,
                            ),
                        ],
                        xs=12,
                        md=6,
                    ),
                ],
                className="g-1 ms-md-3 me-md-3",
            )
        ),
        className="shadow-sm mt-2",
    )
