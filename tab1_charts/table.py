import dash_bootstrap_components as dbc
import duckdb
from queries.queries import temp_table, table_query
from dash_bootstrap_templates import load_figure_template
from dash import html

con = duckdb.connect()
con.execute(temp_table)

load_figure_template()


def table_chart(borough, year_range=None, template=None):
    if not borough:
        borough = ["QUEENS", "BROOKLYN", "MANHATTAN", "BRONX", "STATEN ISLAND"]

    params = (borough,)

    df = con.execute(table_query, parameters=params).df()

    return dbc.Table.from_dataframe(
        df, striped=True, bordered=True, hover=True, responsive=True
    )


def table(borough, year_range, template):
    return dbc.Card(
        dbc.CardBody(
            [
                html.H5(
                    "Recent crashes",
                    className="mb-3",
                ),
                table_chart(borough, year_range, template),
            ]
        ),
        className="mt-3 shadow-sm",
    )
