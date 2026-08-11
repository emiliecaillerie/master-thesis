########################################
# Imports
########################################
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

########################################
# Load and clean data
########################################
df = pd.read_csv('visualization/outputs/dashboard_data.csv', keep_default_na=False)

df['Year'] = pd.to_numeric(df['Year'], errors='coerce').astype(int)
df['Coverage'] = pd.to_numeric(df['Coverage'], errors='coerce').fillna(0.0)
df['Intensity'] = pd.to_numeric(df['Intensity'], errors='coerce')

country_names = dict(zip(df['Country'], df['Country_name']))
hazard_names = dict(zip(df['Hazard'], df['Hazard_name']))
df_hazards = sorted(df['Hazard'].unique())
df_countries = sorted(df['Country'].unique(), key=lambda c: country_names[c])

# Set default values for the initial state of the dashboard
DEFAULT_HAZARD = 'temperature_extremes'
DEFAULT_COUNTRY = 'AUT'

# Fix hazard order for bar chart
HAZARD_LABEL_ORDER = [hazard_names[h] for h in df_hazards]


########################################
# Normalize values and compute gap
########################################
def normalize(var):
    range = var.max() - var.min()
    if range == 0:
        return var * 0.0
    return (var - var.min()) / range

df['NCoverage'] = df.groupby('Hazard')['Coverage'].transform(normalize)
df['NIntensity'] = df.groupby('Hazard')['Intensity'].transform(normalize)

df['Gap'] = df['NCoverage'] - df['NIntensity']
df.loc[df['Intensity'].isna(), ['NIntensity', 'Gap']] = np.nan


########################################
# Map
########################################
def make_map(hazard):
    sub = df[df['Hazard'] == hazard].dropna(subset=['Gap']).sort_values('Year')
    fig = px.choropleth(sub, locations='Country', color='Gap', hover_name='Country_name',
                        animation_frame='Year', color_continuous_scale='RdYlGn', range_color=[-1.0, 1.0],
                        title=f"Map of Policy Gap for {hazard_names.get(hazard, hazard)}")
    fig.update_layout(height=550)
    fig.update_geos(showocean=True, oceancolor='lightblue', showlakes=True, lakecolor='lightblue')
    return fig


########################################
# Timeline
########################################
def symmetric_range(series):
        m = series.abs().max()
        m = m * 1.1 if pd.notna(m) and m > 0 else 1
        return [-m, m]
    
def make_timeline(country, hazard):
    sub = df[(df['Country'] == country) & (df['Hazard'] == hazard)].sort_values('Year')
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=sub['Year'], y=sub['Coverage'], name='Coverage',
                             mode='lines+markers', line=dict(color='green'), yaxis='y1'))
    fig.add_trace(go.Scatter(x=sub['Year'], y=sub['Intensity'], name='Intensity',
                             mode='lines+markers', line=dict(color='red'), yaxis='y2'))
    
    coverage_range = symmetric_range(sub['Coverage'])
    intensity_range = symmetric_range(sub['Intensity'])
    coverage_ticks = np.linspace(coverage_range[0], coverage_range[1], 7)
    intensity_ticks = np.linspace(intensity_range[0], intensity_range[1], 7)
    fig.update_layout(height=450,
        title=f"Timeline of Legislative Coverage and Hazard Intensity<br>for {hazard_names.get(hazard, hazard)} in {country_names.get(country, country)}",
        xaxis=dict(title='Year', fixedrange=True),
        yaxis=dict(title=dict(text='Coverage', font=dict(color='green')), tickfont=dict(color='green'),
                   range=coverage_range, tickmode='array', tickvals=coverage_ticks, 
                   ticktext=np.round(coverage_ticks).astype(int), fixedrange=True),
        yaxis2=dict(title=dict(text='Intensity', font=dict(color='red')), tickfont=dict(color='red'),
                     overlaying='y', side='right', range=intensity_range, tickmode='array', 
                     tickvals=intensity_ticks, ticktext=np.round(intensity_ticks, 2), showgrid=False,
                     fixedrange=True),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1))
    return fig

def make_gap_timeline(country, hazard):
    sub = df[(df['Country'] == country) & (df['Hazard'] == hazard)].sort_values('Year')
    fig = px.line(sub, x='Year', y='Gap', markers=True,
                  title=f"Timeline of Policy Gap<br>for {hazard_names.get(hazard, hazard)} in {country_names.get(country, country)}")
    fig.update_layout(height=450, yaxis_title='Gap', yaxis_range=[-1.05, 1.05],
                      xaxis=dict(fixedrange=True), yaxis=dict(fixedrange=True))
    fig.update_traces(line_color='gold', marker_color='gold')
    fig.add_hline(y=0, line_dash='dash', line_color='grey')
    return fig


########################################
# Bar chart
########################################
def make_bar(country):
    sub = df[df['Country'] == country].sort_values('Year')
    fig = px.bar(sub, x='Hazard_name', y='Gap', color='Gap', color_continuous_scale='RdYlGn', 
                 range_color=[-1.0, 1.0], animation_frame='Year',
                 title=f"Bar Chart of Policy Gap by Hazard in {country_names.get(country, country)}")
    fig.update_layout(height=500, xaxis_title='Hazard', yaxis_title='Gap',
                      yaxis_range=[-1.05, 1.05], xaxis=dict(categoryorder='array', categoryarray=HAZARD_LABEL_ORDER,
                      fixedrange=True), yaxis=dict(fixedrange=True))
    return fig


########################################
# Scatter plot
########################################
def make_scatter(hazard):
    sub = df[df['Hazard'] == hazard].dropna(subset=['NIntensity', 'NCoverage', 'Continent_name', 'Gap']).sort_values('Year')
    fig = px.scatter(sub, x='NIntensity', y='NCoverage', color='Gap', size=sub['Gap'].abs(),
                     hover_name='Country_name', hover_data={'Continent_name': True}, animation_frame='Year',
                     color_continuous_scale='RdYlGn', range_color=[-1.0, 1.0],
                     labels={'NIntensity': 'Normalized intensity', 'NCoverage': 'Normalized coverage',
                             'Continent_name': 'Continent'},
                     title=f"Scatter Plot of Countries' Coverage and Intensity for {hazard_names.get(hazard, hazard)}")
 
    fig.add_shape(type='line', x0=0, y0=0, x1=1, y1=1, line=dict(dash='dash', color='black'))
    fig.update_layout(height=550, xaxis_range=[-0.05, 1.05], yaxis_range=[-0.05, 1.05],
                      xaxis=dict(fixedrange=True), yaxis=dict(fixedrange=True))
    return fig


########################################
# Dashboard layout
########################################
app = Dash(__name__)

hazard_options = [{'label': hazard_names.get(h, h), 'value': h} for h in df_hazards]
country_options = [{'label': country_names.get(c, c), 'value': c} for c in df_countries]

graph_config = {'responsive': True}

app.layout = html.Div(style={'fontFamily': 'Arial, sans-serif', 'margin': '20px'}, children=[
    # Title
    html.H1("Visualization Dashboard"),
    
    # Source
    html.H3("Data Sources:"), 
    html.P([html.A(href="https://climate-laws.org/", target="_blank", children="Climate Change Laws of the World"), 
           " (Apr. 2026) and ", html.A(href="https://climatepolicydatabase.org/policies", target="_blank", children="Climate Policy Database"),
            " (Apr. 2026) for legislative data, ", html.A(href="https://cds.climate.copernicus.eu/datasets", target="_blank", children="Climate Data Store"),
            " (May 2026) for sensor data"]),
    
    # Definitions
    html.H3("Definitions:"),
    html.P("Legislative Coverage = the cumulative count of laws per country per hazard category per year"),
    html.P("Hazard Intensity =  the deviation of the climate variable associated with each hazard category, relative to a historical baseline period"),
    html.P("Policy Gap = (Normalized legislative coverage) - (Normalized hazard intensity)"),

    # Hazard and country slicers
    html.Div(style={'marginBottom': '20px'}, children=[
        html.Label("Select Hazard:", style={'fontWeight': 'bold', 'marginRight': '8px'}),
        dcc.Dropdown(
            id='hazard-dropdown', options=hazard_options, value=DEFAULT_HAZARD,
            clearable=False, style={'width': '280px', 'display': 'inline-block', 'marginRight': '30px'},
        ),
        html.Label("and Country:", style={'fontWeight': 'bold', 'marginRight': '8px'}),
        dcc.Dropdown(
            id='country-dropdown', options=country_options, value=DEFAULT_COUNTRY,
            clearable=False, style={'width': '280px', 'display': 'inline-block'},
        ),
    ]),

    # Map
    dcc.Graph(id='map-graph', config=graph_config),

    # Both timelines side by side
    html.Div(style={'display': 'flex', 'gap': '20px', 'marginTop': '20px'}, children=[
        html.Div(dcc.Graph(id='timeline-graph', config=graph_config), style={'flex': 1, 'minWidth': 0}),
        html.Div(dcc.Graph(id='gap-timeline-graph', config=graph_config), style={'flex': 1, 'minWidth': 0}),
    ]),

    # Bar chart and scatter plot side by side
    html.Div(style={'display': 'flex', 'gap': '20px', 'marginTop': '20px'}, children=[
        html.Div(dcc.Graph(id='bar-graph', config=graph_config), style={'flex': 1, 'minWidth': 0}),
        html.Div(dcc.Graph(id='scatter-graph', config=graph_config), style={'flex': 1, 'minWidth': 0}),
    ]),
    
    # Source
    html.P(["Data Sources: ", html.A(href="https://climate-laws.org/", target="_blank", children="Climate Change Laws of the World"), 
           " (Apr. 2026) and ", html.A(href="https://climatepolicydatabase.org/policies", target="_blank", children="Climate Policy Database"),
            " (Apr. 2026) for legislative data, ", html.A(href="https://cds.climate.copernicus.eu/datasets", target="_blank", children="Climate Data Store"),
            " (May 2026) for sensor data"])
])


########################################
# Callbacks
########################################
@app.callback(
    Output('map-graph', 'figure'),
    Output('scatter-graph', 'figure'),
    Input('hazard-dropdown', 'value'),
)
def update_hazard_driven_charts(hazard):
    return make_map(hazard), make_scatter(hazard)


@app.callback(
    Output('bar-graph', 'figure'),
    Input('country-dropdown', 'value'),
)
def update_country_driven_charts(country):
    return make_bar(country)


@app.callback(
    Output('timeline-graph', 'figure'),
    Output('gap-timeline-graph', 'figure'),
    Input('country-dropdown', 'value'),
    Input('hazard-dropdown', 'value'),
)
def update_timeline_charts(country, hazard):
    return make_timeline(country, hazard), make_gap_timeline(country, hazard)


if __name__ == '__main__':
    app.run(debug=True)