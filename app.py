# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.


from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

app = Dash()

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

regions = []
dates = []
sales = []
# read the filtered data from CSV
filtered_file_path = "data/filtered_data.csv"
df = pd.read_csv(filtered_file_path)
# loop through columns and create a list of dates, regions, sales
for index, row in df.iterrows():
    dates.append(row["Date"])
    regions.append(row["Region"])
    sales.append(row["Sales"])

df = pd.DataFrame({
    "Date": dates,
    "Sales": sales,
    "Region": regions
})

fig = px.bar(df, x="Date", y="Sales", color="Region", barmode="group")

app.layout = html.Div(children=[
    html.H1(children='Soul Foods Pink Morsels Sales Dashboard'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run(debug=True)

