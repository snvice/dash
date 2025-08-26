import dash_bootstrap_components as dbc
from tab1_charts.kpi_cards import kpi_cards
from tab1_charts.word_cloud import word_bar
from tab1_charts.pie import pie
from tab1_charts.table import table
import plotly.express as px
import duckdb
from queries.queries import temp_table, map_query
from dash import dcc


external_css = [
    "https://unpkg.com/leaflet.markercluster@1.4.1/dist/MarkerCluster.Default.css",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css",
]


fa_icon = dict(
    html='<i class="fa-solid fa-building fa-2x text-danger"></i>',
    className="",
    iconSize=[30, 30],
)


def tab1_content(borough, year_range, template):
    return dbc.Container(
        fluid=True,
        children=[
            kpi_cards(borough, year_range),
            word_bar(borough, year_range, template),
            pie(borough, year_range, template),
            table(borough, year_range, template),
        ],
    )


con = duckdb.connect()
con.execute(temp_table)


def map(borough, year_range, template):
    start_year, end_year = year_range

    if not borough:
        borough = ["QUEENS", "BROOKLYN", "MANHATTAN", "BRONX", "STATEN ISLAND"]

    params = (borough, start_year, end_year)

    mapdf = con.execute(map_query, parameters=params).df()

    return (
        px.scatter_map(
            mapdf,
            lat="LATITUDE",
            lon="LONGITUDE",
            color="BOROUGH",
            center={"lat": 40.7128, "lon": -74.0060},  # Center on NYC
            # size='NUMBER OF PERSONS KILLED',
            # size_max=15,
            zoom=9.5,
            height=700,
            title="NYC Traffic Collisions by Borough",
            template=template,
            map_style="open-street-map",  #'carto-positron', #'open-street-map',  #'carto-positron',
            color_discrete_sequence=px.colors.qualitative.Prism,
            # color_discrete_sequence=px.colors.qualitative.Antique,
            hover_data=[
                "ON STREET NAME",
                "NUMBER OF PERSONS INJURED",
                "NUMBER OF PERSONS KILLED",
                "CONTRIBUTING FACTOR VEHICLE 1",
                "VEHICLE TYPE CODE 1",
            ],
            # hover_name='BOROUGH',
        )
        .update_traces(
            cluster=dict(enabled=True, step=50, size=20), marker=dict(size=20)
        )
        .update_layout(
            margin=dict(b=20, l=10, r=10),
            # showlegend=False,
            legend=dict(orientation="h", y=1, yanchor='bottom'),
            legend_title=None
        )
    )


def tab2_content(borough, year_range, template):
    return dbc.Container(
        fluid=True,
        children=[
            dbc.Card(
                dbc.CardBody(
                    [
                        dcc.Graph(
                            figure=map(borough, year_range, template),
                            config={"displayModeBar": False},
                            
                        )
                    ]
                    # dl.Map(
                    #     children=[
                    #         # dl.TileLayer(),
                    #         # dl.GeoJSON(
                    #         #     url="/assets/offices.json",
                    #         #     cluster=True,
                    #         #     zoomToBoundsOnClick=True,
                    #         #     superClusterOptions={"radius": 100},
                    #         # ),
                    #         # dl.DivMarker(
                    #         #     position=[-1.2921, 36.8219], iconOptions=fa_icon
                    #         # ),
                    #     ],
                    #     center=[-0.02, 37.91],
                    #     zoom=6,
                    #     style={"height": "60vh", "width": "100%"},
                    # )
                ),
                className="mt-3 shadow-sm",
            )
        ],
    )
