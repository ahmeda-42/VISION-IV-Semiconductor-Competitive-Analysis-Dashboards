# Vision IV Diamond Dopants Semiconductor Performance Explorer
# VERSION 4.0
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import numpy as np

# Sample data
materials_data = pd.DataFrame({
    # Material
    'Material': [
        'Undoped Diamond', 
        'Boron-Doped Diamond (BDD)',
        'Phosphorus-Doped Diamond (PDD)',
        'Nitrogen-Doped Diamond (NDD)',
        'HPHT Diamond',
        'CVD Diamond'
    ],
    
    # General Operating Metrics 
    'Max Temperature': [1000, 950, 940, 900, 950, 980],  # °C
    'Breakdown Voltage': [2000, 1950, 1900, 1700, 1800, 1900],  # V
    'Max Frequency': [1000, 1200, 1150, 800, 950, 1000],  # GHz
    
    # Radiation Hardness 
    "TID Tolerance": [1e7, 1e7, 9e6, 8e6, 9.5e6, 9.8e6],  # rad(Si)
    "DDD Tolerance": [1e16, 1e16, 9.5e15, 8e15, 9e15, 9.7e15],  # n/cm²
    "LET Threshold": [100, 96, 92, 85, 90, 98],  # MeV·cm²/mg
    "Displacement Threshold Energy": [43, 42, 41, 40, 41, 42],  # eV
    
    # Electronic Properties
    'Bandgap': [5.45, 5.0, 4.9, 4.8, 5.3, 5.4],  # eV
    'Breakdown Field': [1000, 975, 960, 850, 900, 980],  # MV/m
    'Electron Mobility': [0.22, 0.25, 0.21, 0.15, 0.20, 0.22],  # m²/V·s
    'Base Power Density': [5000, 4900, 4800, 4000, 4500, 4950],  # W/cm²
    'Thermal Conductivity': [2200, 2000, 1900, 1500, 2100, 2150],  # W/m·K
})

# Define Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Vision IV Diamond Dopants Semiconductor Performance Explorer", style={'textAlign': 'center'}),

    html.H2("General Operating Metrics", style={'textAlign': 'left'}),

    html.Div([
        html.Label("Operating Temperature (°C):"),
        dcc.Slider(id='temperature-slider', min=900, max=1000, step=2, value=950,
                   tooltip={"placement": "bottom", "always_visible": True})
    ], style={'padding': 20}),

    html.Div([
        html.Label("Operating Voltage (V):"),
        dcc.Slider(id='voltage-slider', min=1700, max=2000, step=10, value=1850,
                   tooltip={"placement": "bottom", "always_visible": True},
                   marks={i: str(i) for i in range(1700, 2001, 10)})
    ], style={'padding': 20}),

    html.Div([
        html.Label("Operating Frequency (GHz):"),
        dcc.Slider(id='frequency-slider', min=800, max=1200, step=10, value=1000,
                   tooltip={"placement": "bottom", "always_visible": True},
                   marks={i: str(i) for i in range(800, 1201, 10)})
    ], style={'padding': 20}),

    html.Div([
        dcc.Graph(id='temp-performance-bar'),
        dcc.Graph(id='voltage-performance-bar'),
        dcc.Graph(id='frequency-performance-bar'),
    ]),

    html.H2("Radiation Hardness Metrics", style={'textAlign': 'left'}),

    html.Div([
        html.Label("Total Ionizing Dose (rad(Si)):"),
        dcc.Slider(id='TID-slider', min=8e6, max=1e7, step=100000, value=9e6,
                   tooltip={"placement": "bottom", "always_visible": True},
                   marks={i: f"{i/1e6:.2f}M" for i in range(8_000_000, 10_000_001, 100_000)})
    ], style={'padding': 20}),

    html.Div([
        html.Label("Displacement Damage Dose (n/cm²):"),
        dcc.Slider(id='DDD-slider', min=8e15, max=1e16, step=1e14, value=9e15,
                   tooltip={"placement": "bottom", "always_visible": True},
                   marks={i: f"{i/1e15:.2f}P" for i in range(int(8e15), int(1e16) + 1, int(1e14))})
    ], style={'padding': 20}),

    html.Div([
        html.Label("Linear Energy Transfer (MeV·cm²/mg):"),
        dcc.Slider(id='LET-slider', min=85, max=100, step=0.5, value=92.5,
                   tooltip={"placement": "bottom", "always_visible": True})
    ], style={'padding': 20}),

    html.Div([
        html.Label("Displacement Energy (eV):"),
        dcc.Slider(id='DE-slider', min=40, max=43, step=0.125, value=41.5,
                   tooltip={"placement": "bottom", "always_visible": True})
    ], style={'padding': 20}),

    html.Div([
        dcc.Graph(id='TID-performance-bar'),
        dcc.Graph(id='DDD-performance-bar'),
        dcc.Graph(id='LET-performance-bar'),
        dcc.Graph(id='DE-performance-bar'),
    ]),
])

@app.callback(
    [Output('temp-performance-bar', 'figure'),
     Output('voltage-performance-bar', 'figure'),
     Output('frequency-performance-bar', 'figure'),
     Output('TID-performance-bar', 'figure'),
     Output('DDD-performance-bar', 'figure'),
     Output('LET-performance-bar', 'figure'),
     Output('DE-performance-bar', 'figure')],
    [Input('temperature-slider', 'value'),
     Input('voltage-slider', 'value'),
     Input('frequency-slider', 'value'),
     Input('TID-slider', 'value'),
     Input('DDD-slider', 'value'),
     Input('LET-slider', 'value'),
     Input('DE-slider', 'value')]
)

def update_graphs(temp, voltage, freq, TID, DDD, LET, DE):
    df = materials_data.copy()

    # === Performance due to Temperature ===
    df['Temp Performance'] = df.apply(
        lambda row: 1 if row['Max Temperature'] > temp else (row['Max Temperature'] / temp),
        axis=1)
    fig1 = go.Figure()
    fig1.add_trace(go.Bar(x=df['Material'], y=df['Temp Performance'], marker_color='royalblue'))
    fig1.update_layout(title='Performance due to Operating Temperature',
                       yaxis_title='Relative Performance', xaxis_title='Material')

    # === Performance due to Voltage ===
    df['Voltage Performance'] = df.apply(
        lambda row: 1 if row['Breakdown Voltage'] > voltage else (row['Breakdown Voltage'] / voltage),
        axis=1)
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(x=df['Material'], y=df['Voltage Performance'], marker_color='seagreen'))
    fig2.update_layout(title='Performance due to Operating Voltage',
                       yaxis_title='Relative Performance', xaxis_title='Material')

    # === Performance due to Frequency ===
    df['Frequency Performance'] = df.apply(
        lambda row: 1 if row['Max Frequency'] > freq else (row['Max Frequency'] / freq),
        axis=1)
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(x=df['Material'], y=df['Frequency Performance'], marker_color='firebrick'))
    fig3.update_layout(title='Performance due to Operating Frequency',
                       yaxis_title='Relative Performance', xaxis_title='Material')

    # === Performance due to TID ===
    df['TID Performance'] = df.apply(
        lambda row: 1 if row['TID Tolerance'] > TID else (row['TID Tolerance'] / TID),
        axis=1)
    fig4 = go.Figure()
    fig4.add_trace(go.Bar(x=df['Material'], y=df['TID Performance'], marker_color='Chocolate'))
    fig4.update_layout(title='Performance due to Total Ionizing Dose',
                       yaxis_title='Relative Performance', xaxis_title='Material')
    
    # === Performance due to DDD ===
    df['DDD Performance'] = df.apply(
        lambda row: 1 if row['DDD Tolerance'] > DDD else (row['DDD Tolerance'] / DDD),
        axis=1)
    fig5 = go.Figure()
    fig5.add_trace(go.Bar(x=df['Material'], y=df['DDD Performance'], marker_color='Tomato'))
    fig5.update_layout(title='Performance due to Displacement Damage Dose',
                       yaxis_title='Relative Performance', xaxis_title='Material')

    # === Performance due to LET ===
    df['LET Performance'] = df.apply(
        lambda row: 1 if row['LET Threshold'] > LET else (row['LET Threshold'] / LET),
        axis=1)
    fig6 = go.Figure()
    fig6.add_trace(go.Bar(x=df['Material'], y=df['LET Performance'], marker_color='Crimson'))
    fig6.update_layout(title='Performance due to Linear Energy Transfer',
                       yaxis_title='Relative Performance', xaxis_title='Material')
    
    # === Performance due to DE ===
    df['DE Performance'] = df.apply(
        lambda row: 1 if row['Displacement Threshold Energy'] > DE else (row['Displacement Threshold Energy'] / DE),
        axis=1)
    fig7 = go.Figure()
    fig7.add_trace(go.Bar(x=df['Material'], y=df['DE Performance'], marker_color='DeepPink'))
    fig7.update_layout(title='Performance due to Displacement Energy',
                       yaxis_title='Relative Performance', xaxis_title='Material')

    return fig1, fig2, fig3, fig4, fig5, fig6, fig7

if __name__ == '__main__':
    app.run(debug=True)