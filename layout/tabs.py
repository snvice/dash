import dash_bootstrap_components as dbc


def tabs():
    return dbc.CardBody(
        dbc.Tabs(
            children=[
                dbc.Tab(
                    label="Crash Statistics",
                    tab_id="tab1",
                    tab_style={"width": "50%", "textAlign": "center"},
                    activeTabClassName="fw-bold",
                    active_label_style={
                        "textDecoration": "underline",
                        "color": "#FFC107",
                        "textTransform": "none",
                    },
                ),
                dbc.Tab(
                    label="Map",
                    tab_id="tab2",
                    tab_style={"width": "50%", "textAlign": "center"},
                    activeTabClassName="fw-bold",
                    active_label_style={
                        "textDecoration": "underline",
                        "color": "#FFC107",
                        "textTransform": "none",
                    },
                ),
            ],
            id="Tabs",
            active_tab="tab1",
        ),
        className="mt-2",
    )
