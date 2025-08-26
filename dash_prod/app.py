from layout.header import header, theme_switch_component
from layout.filter import filters
from layout.tabs import tabs
from dash import html, Input, Output
import dash_bootstrap_components as dbc
from tab_content.tab1_content import tab1_content, tab2_content
from dash_bootstrap_templates import ThemeSwitchAIO
from dash_extensions.enrich import DashProxy


icons = "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css"


app = DashProxy(external_stylesheets=[dbc.themes.SANDSTONE, icons])
app.title = "NYC Vehicle Collisions Analysis"

app.layout = dbc.Container(
    fluid=True,
    children=[
        theme_switch_component(),
        header(),
        filters(),
        tabs(),
        html.Div(id="content", style={"overflowY": "auto", "maxHeight": "800px"}),
    ],
)


@app.callback(
    Output("content", "children"),
    [
        Input("Tabs", "active_tab"),
        Input(ThemeSwitchAIO.ids.switch("theme"), "value"),
        Input("borough-checklist", "value"),
        Input("year-range", "value"),
    ],
    # prevent_initial_call=True
)
def switch_tab(active_tab, toggle, borough, year_range):
    if active_tab == "tab1":
        template = "sandstone" if toggle else "slate"
        return tab1_content(borough, year_range, template)
    elif active_tab == "tab2":
        template = "sandstone" if toggle else "slate"
        return tab2_content(borough, year_range, template)


if __name__ == "__main__":
    app.run(debug=True)
