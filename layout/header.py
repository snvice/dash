from datetime import datetime
import dash_bootstrap_components as dbc
from dash import html
from dash_bootstrap_templates import ThemeSwitchAIO


current_dateTime = datetime.now()


def theme_switch_component():
    return dbc.Row(
        [
            dbc.Col(
                [
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                    html.Div(
                                        [
                                            html.Span(
                                                "Theme",
                                                className="me-3 small",
                                            ),
                                            ThemeSwitchAIO(
                                                aio_id="theme",
                                                themes=[
                                                    dbc.themes.SANDSTONE,
                                                    dbc.themes.SLATE,
                                                ],
                                                switch_props={"persistence": True},
                                                icons={
                                                    "left": "fa fa-moon text-light",
                                                    "right": "fa fa-sun text-warning",
                                                },
                                            ),
                                        ],
                                        className="d-flex align-items-center justify-content-end",
                                    )
                                ],
                                className="p-2",
                            )
                        ],
                        className="border-1 shadow",
                    )
                ],
                width="auto",
            )
        ],
        className="mb-1 mt-1",
        justify="end",
    )


def header():
    return dbc.Card(
        dbc.CardBody(
            children=[
                dbc.Row(
                    [
                        html.H1(
                            [
                                html.Span("NYC Motor Vehicles Crashes Dashboard"),
                                html.I(
                                    className="fa-solid fa-car-on ms-1",
                                    style={"color": "#FFC107"},
                                ),
                            ],
                            className="mb-0 fs-3 fw-bold",
                        ),
                    ],
                    className="align-items-center",
                ),
                html.P(
                    "Real-time analysis of traffic incidents across New York City",
                    className="mt-1 mb-0",
                ),
                html.Small(
                    [
                        html.I(
                            className="fa-solid fa-arrows-rotate me-1",
                            style={"color": "#FFC107"},
                        ),
                        # f"Last Updated: Today at {current_dateTime.strftime('%I:%M %p')}",
                        "Last Updated: June 22 2025",
                    ],
                    className="text-muted mt-1",
                ),
            ],
            className="text-center border-0 shadow-sm",
        )
    )
