# import required dependencies
import pandas as pd
import numpy as np
import plotly.express as px
from dash import Dash, html, dcc, Input, Output, callback

# read the data
df = pd.read_csv('data/cleaned_data.csv')

# initialize the Dash app -- incorporate css
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(className='row', children=[
    html.Br(),
    html.H1(children='Singapore Resale HDB Analysis', style={'text-align': 'center'}),

    html.Div(className='row', children=[
        html.Div(className='one columns', children=[html.Br()]),
        html.Div(className='three columns', children=[
            html.Div(children=[
                html.H3('Select year'),
                dcc.Slider(
                    df['year'].min(),
                    df['year'].max(),
                    step=None,
                    value=df['year'].min(),
                    marks={str(year): str(year) for year in df['year'].unique()},
                    id='year-slider'
                ),
                html.Br(),
                html.H3('Select town'),
                dcc.RadioItems(
                    options=[{'label': town, 'value': town} for town in df['town'].unique()],
                    value = df['town'].unique()[0],
                    id='area-radio'
                )
            ])
        ]),
        html.Div(className='seven columns', children=[
            dcc.Graph(id='box-plot'),
            html.Br(),
            dcc.Graph(id='bar-chart'),
            html.Br(),
            dcc.Graph(id='scatter-plot'),
            html.Br(),
            dcc.Graph(id='scatter-plot-lease'),
            html.Br(),
            dcc.Graph(id='bar-chart-flat'),
        ]),
        html.Div(className='one columns', children=[html.Br()])
    ])
])

# Figure 1 --- Box plot
@app.callback(
    Output('box-plot', 'figure'),
    Input('year-slider', 'value')
)
def update_box(selected_year):
    filtered_df = df[df['year'] == selected_year]
    box = px.box(filtered_df,
                 x='town', y='price_per_sqm',
                 color='town',
                 height=650,
                 title=f'Year {selected_year}: Price / Square per Meter')
    box.update_layout(
        xaxis=dict(
            title='Town'
        ),
        yaxis=dict(
            title='Price per sqm'
        )
    )
    return box

# Figure 2 --- Bar Chart
@app.callback(
    Output('bar-chart', 'figure'),
    Input('area-radio', 'value')
)
def update_bar(selected_town):
    filtered_df = df[df['town'] == selected_town]

    selected = filtered_df['year'].value_counts().sort_index()
    selected_df = pd.DataFrame(selected).reset_index()
    selected_df.columns = ['Year', 'Count']
    bar = px.bar(selected_df, 
                 x='Year', y='Count', 
                 height=400,
                 title=f'Number of Resale HDB Units in {selected_town} Over the Years')

    bar.update_layout(
        xaxis = dict(
            title = 'Year'
        ),
        yaxis = dict(
            title = 'Count'
        )
    )
    bar.update_traces(marker_color='purple')
    return bar

# Figure 3 --- Scatter plot (MRT Distance vs Price per sqm)
@app.callback(
    Output('scatter-plot', 'figure'),
    Input('year-slider', 'value'),
    Input('area-radio', 'value')
)
def update_scatter(selected_year, selected_town):
    filtered_df = df[(df['year'] == selected_year) & (df['town'] == selected_town)]
    scatter = px.scatter(data_frame=filtered_df,
                         x='mrt_dist', y='price_per_sqm',
                         size='price_per_sqm', color='flat_type',
                         height=1000,
                         title=f'Year {selected_year}: MRT Distance vs Price per sqm in {selected_town}')
    scatter.update_layout(
        xaxis=dict(
            title='MRT Distance'
        ),
        yaxis=dict(
            title='Price per sqm'
        )
    )
    return scatter

# Figure 4 --- Scatter plot (Remaining Lease (Month vs Price per sqm))
@app.callback(
    Output('scatter-plot-lease', 'figure'),
    Input('year-slider', 'value'),
    Input('area-radio', 'value')
)
def update_scatter_lease(selected_year, selected_town):
    filtered_df = df[(df['year'] == selected_year) & (df['town'] == selected_town)]
    scatter_lease = px.scatter(data_frame=filtered_df, 
                               x='remaining_lease_month', y='price_per_sqm', 
                               color = 'street_name',
                               height=800, 
                               title=f'Year {selected_year}: Price per sqm vs Remaining Lease (Months) in {selected_town}')

    scatter_lease.update_layout(
        xaxis = dict(
            title = 'Remaining Lease (Months)'
        ),
        yaxis = dict(
            title = 'Price per sqm'
        )
    )
    return scatter_lease


# Figure 5 --- Bar Chart
@app.callback(
    Output('bar-chart-flat', 'figure'),
    Input('year-slider', 'value'),
    Input('area-radio', 'value')
)
def update_bar_flattype(selected_year, selected_town):
    filtered_df = df[(df['year'] == selected_year) & (df['town'] == selected_town)]
    
    flat_type = filtered_df['flat_type'].value_counts().sort_index()
    flat_type_df = pd.DataFrame(flat_type).reset_index()
    flat_type_df.columns = ['Flat_Type', 'Count']

    bar_flat = px.bar(flat_type_df, 
                 x='Flat_Type', y='Count', 
                 height=500, 
                 title=f'Year {selected_year}: Distribution of Resale HDB by Flat Type in {selected_town}')
    
    bar_flat.update_layout(
        xaxis = dict(
            title = 'Flat Type'
        ),
        yaxis = dict(
            title = 'Count'
        )
    )
    bar_flat.update_traces(marker_color='orange')
    return bar_flat




# run the app
if __name__ == '__main__':
    app.run(debug=True)
