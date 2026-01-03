# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

app = Dash(__name__)

# Read filtered data from CSV
filtered_file_path = "data/filtered_data.csv"
df = pd.read_csv(filtered_file_path)

# Ensure Date is a datetime for proper plotting and sorting
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values(by="Date")

# Keep a lowercase Region helper for case-insensitive filtering
df["_region_lower"] = df["Region"].astype(str).str.lower()

# Initial figure: a line chart showing Sales over time by Region
fig = px.line(df, x="Date", y="Sales", color="Region", markers=True)

app.layout = html.Div(className="container", children=[
    html.H1(children='Soul Foods Pink Morsels Sales Dashboard', className="header"),

    html.Div(children='A small interactive dashboard to explore Pink Morsels sales by region.', className="subheader"),

    html.Div(className="controls", children=[
        html.Label("Select region:", className="radio-label"),
        dcc.RadioItems(
            id='region-radio',
            options=[
                {'label': 'North', 'value': 'north'},
                {'label': 'East',  'value': 'east'},
                {'label': 'South', 'value': 'south'},
                {'label': 'West',  'value': 'west'},
                {'label': 'All',   'value': 'all'},
            ],
            value='all',
            labelStyle={'display': 'inline-block'},
            className='radio-items'
        )
    ]),

    html.Div(className="chart-card", children=[
        dcc.Graph(
            id='sales-graph',
            figure=fig,
            config={'displayModeBar': False}
        )
    ]),
])


@app.callback(
    Output('sales-graph', 'figure'),
    Input('region-radio', 'value')
)
def update_figure(selected_region):
    """Update the line chart based on the selected region.

    - selected_region: one of 'north', 'east', 'south', 'west', 'all'
    - returns: Plotly figure filtered accordingly
    """
    if selected_region == 'all':
        filtered = df
    else:
        filtered = df[df['_region_lower'] == selected_region]

    # If filtered is empty, return an empty figure with a helpful message
    if filtered.empty:
        empty_fig = px.line()
        empty_fig.update_layout(
            title=f"No data available for '{selected_region}'",
            xaxis_title='Date',
            yaxis_title='Sales'
        )
        return empty_fig

    fig = px.line(filtered, x='Date', y='Sales', color='Region', markers=True)
    fig.update_layout(transition_duration=300, xaxis=dict(tickformat='%Y-%m-%d'))
    return fig


if __name__ == '__main__':
    app.run(debug=True)

