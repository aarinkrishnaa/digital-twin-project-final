import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import pandas as pd
import random
import numpy as np

app = dash.Dash(__name__)
server = app.server

# Modern dark theme colors
DARK_BG = '#0a0a0a'
CARD_BG = '#141414'
TEXT_PRIMARY = '#ffffff'
TEXT_SECONDARY = '#9ca3af'
ACCENT_BLUE = '#3b82f6'
ACCENT_GREEN = '#10b981'
ACCENT_RED = '#ef4444'
ACCENT_ORANGE = '#f59e0b'

# Global motor state
motor_running = False
target_rpm = 1500

app.layout = html.Div([
    # Header
    html.H1("Smart Factory Digital Twin - Demo", 
           style={'color': TEXT_PRIMARY, 'textAlign': 'center', 'background': 'linear-gradient(135deg, #141414 0%, #1a1a1a 100%)', 'padding': '40px', 'margin': '0', 'fontSize': '32px', 'fontWeight': '300', 'letterSpacing': '1px', 'borderBottom': '1px solid #1f1f1f'}),
    
    # Motor Control Panel
    html.Div([
        html.H3("Motor Control", style={'color': TEXT_PRIMARY, 'marginBottom': '24px', 'fontSize': '18px', 'fontWeight': '500'}),
        html.Div([
            html.Button("Start", id='start-btn', n_clicks=0, 
                       style={'background': ACCENT_GREEN, 'color': 'white', 'padding': '12px 24px', 'margin': '0 8px', 'border': 'none', 'borderRadius': '6px', 'fontSize': '14px', 'cursor': 'pointer', 'fontWeight': '500'}),
            html.Button("Stop", id='stop-btn', n_clicks=0,
                       style={'background': ACCENT_RED, 'color': 'white', 'padding': '12px 24px', 'margin': '0 8px', 'border': 'none', 'borderRadius': '6px', 'fontSize': '14px', 'cursor': 'pointer', 'fontWeight': '500'})
        ], style={'marginBottom': '24px'}),
        html.Label("Target RPM", style={'color': TEXT_SECONDARY, 'fontSize': '14px', 'fontWeight': '500', 'marginBottom': '12px', 'display': 'block'}),
        dcc.Slider(id='rpm-slider', min=0, max=2000, value=1500, step=100, 
                  marks={i: {'label': str(i), 'style': {'color': TEXT_SECONDARY, 'fontSize': '12px'}} for i in range(0, 2001, 500)}),
        html.Div(id='motor-status', style={'color': TEXT_PRIMARY, 'fontSize': '16px', 'marginTop': '24px', 'fontWeight': '500'})
    ], style={'background': CARD_BG, 'padding': '32px', 'margin': '24px', 'borderRadius': '8px', 'border': '1px solid #1f1f1f'}),
    
    # KPI Cards
    html.Div([
        html.Div([
            html.Div("Temperature", style={'color': TEXT_SECONDARY, 'fontSize': '12px', 'fontWeight': '500', 'marginBottom': '8px', 'textTransform': 'uppercase', 'letterSpacing': '0.5px'}),
            html.Div(id='temp-display', children="22.0°C", style={'color': ACCENT_RED, 'fontSize': '24px', 'fontWeight': '600'})
        ], style={'background': CARD_BG, 'padding': '24px', 'margin': '12px', 'borderRadius': '8px', 'flex': '1', 'border': '1px solid #1f1f1f'}),
        
        html.Div([
            html.Div("Vibration", style={'color': TEXT_SECONDARY, 'fontSize': '12px', 'fontWeight': '500', 'marginBottom': '8px', 'textTransform': 'uppercase', 'letterSpacing': '0.5px'}),
            html.Div(id='vib-display', children="0.0 mm/s", style={'color': ACCENT_BLUE, 'fontSize': '24px', 'fontWeight': '600'})
        ], style={'background': CARD_BG, 'padding': '24px', 'margin': '12px', 'borderRadius': '8px', 'flex': '1', 'border': '1px solid #1f1f1f'}),
        
        html.Div([
            html.Div("Motor Speed", style={'color': TEXT_SECONDARY, 'fontSize': '12px', 'fontWeight': '500', 'marginBottom': '8px', 'textTransform': 'uppercase', 'letterSpacing': '0.5px'}),
            html.Div(id='rpm-display', children="0 RPM", style={'color': ACCENT_GREEN, 'fontSize': '24px', 'fontWeight': '600'})
        ], style={'background': CARD_BG, 'padding': '24px', 'margin': '12px', 'borderRadius': '8px', 'flex': '1', 'border': '1px solid #1f1f1f'}),
        
        html.Div([
            html.Div("Current", style={'color': TEXT_SECONDARY, 'fontSize': '12px', 'fontWeight': '500', 'marginBottom': '8px', 'textTransform': 'uppercase', 'letterSpacing': '0.5px'}),
            html.Div(id='current-display', children="0.0 A", style={'color': ACCENT_ORANGE, 'fontSize': '24px', 'fontWeight': '600'})
        ], style={'background': CARD_BG, 'padding': '24px', 'margin': '12px', 'borderRadius': '8px', 'flex': '1', 'border': '1px solid #1f1f1f'})
    ], style={'display': 'flex', 'padding': '0 12px'}),
    
    # Charts
    html.Div([
        html.Div([
            html.H3("Sensor Trends", style={'color': TEXT_PRIMARY, 'marginBottom': '20px', 'fontSize': '18px', 'fontWeight': '500'}),
            dcc.Graph(id='trends-chart', style={'height': '400px'})
        ], style={'background': CARD_BG, 'padding': '24px', 'margin': '12px', 'borderRadius': '8px', 'flex': '2', 'border': '1px solid #1f1f1f'}),
        
        html.Div([
            html.H3("RPM Gauge", style={'color': TEXT_PRIMARY, 'marginBottom': '20px', 'fontSize': '18px', 'fontWeight': '500'}),
            dcc.Graph(id='rpm-gauge', style={'height': '400px'})
        ], style={'background': CARD_BG, 'padding': '24px', 'margin': '12px', 'borderRadius': '8px', 'flex': '1', 'border': '1px solid #1f1f1f'})
    ], style={'display': 'flex', 'padding': '0 12px'}),
    
    dcc.Interval(id='interval', interval=2000, n_intervals=0)
], style={'fontFamily': 'Inter, -apple-system, BlinkMacSystemFont, sans-serif', 'background': DARK_BG, 'minHeight': '100vh'})

# Motor control callback
@app.callback(
    Output('motor-status', 'children'),
    [Input('start-btn', 'n_clicks'),
     Input('stop-btn', 'n_clicks'),
     Input('rpm-slider', 'value')]
)
def control_motor(start_clicks, stop_clicks, rpm_value):
    global motor_running, target_rpm
    
    ctx = dash.callback_context
    if ctx.triggered:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if button_id == 'start-btn':
            motor_running = True
        elif button_id == 'stop-btn':
            motor_running = False
        
        target_rpm = rpm_value or 1500
    
    status = f"🟢 Motor Running - Target: {target_rpm} RPM" if motor_running else f"🔴 Motor Stopped - Target: {target_rpm} RPM"
    return status

# Dashboard updates
@app.callback(
    [Output('trends-chart', 'figure'),
     Output('rpm-gauge', 'figure'),
     Output('temp-display', 'children'),
     Output('vib-display', 'children'),
     Output('rpm-display', 'children'),
     Output('current-display', 'children')],
    [Input('interval', 'n_intervals')]
)
def update_dashboard(n):
    global motor_running, target_rpm
    
    if motor_running:
        current_rpm = target_rpm + random.randint(-50, 50)
        temp = 70 + random.randint(-10, 10)
        vib = 3.5 + random.uniform(-1, 1)
        current = 12 + random.uniform(-2, 2)
        
        trend_data = pd.DataFrame({
            'temp': np.random.normal(temp, 3, 50),
            'vib': np.random.normal(vib, 0.5, 50),
            'current': np.random.normal(current, 1, 50)
        })
        line_style = dict(width=3)
    else:
        current_rpm = 0
        temp = 22
        vib = 0.0
        current = 0.0
        
        trend_data = pd.DataFrame({
            'temp': [22] * 50,
            'vib': [0] * 50,
            'current': [0] * 50
        })
        line_style = dict(width=3, dash='dot')
    
    # Trends Chart
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(y=trend_data['temp'], name='Temperature (°C)', 
                             line=dict(color=ACCENT_RED, **line_style)))
    fig1.add_trace(go.Scatter(y=trend_data['vib'], name='Vibration (mm/s)', 
                             line=dict(color=ACCENT_BLUE, **line_style)))
    fig1.add_trace(go.Scatter(y=trend_data['current'], name='Current (A)', 
                             line=dict(color=ACCENT_ORANGE, **line_style)))
    
    fig1.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=TEXT_SECONDARY),
        xaxis=dict(gridcolor='#1f1f1f', showgrid=True, color=TEXT_SECONDARY, zeroline=False),
        yaxis=dict(gridcolor='#1f1f1f', showgrid=True, color=TEXT_SECONDARY, zeroline=False),
        legend=dict(font=dict(color=TEXT_SECONDARY)),
        margin=dict(l=40, r=40, t=20, b=40)
    )
    
    # RPM Gauge
    gauge_color = ACCENT_GREEN if motor_running else '#666666'
    fig2 = go.Figure(go.Indicator(
        mode="gauge+number",
        value=current_rpm,
        title={'text': "RPM", 'font': {'color': TEXT_SECONDARY, 'size': 20}},
        number={'font': {'color': TEXT_PRIMARY, 'size': 36}},
        gauge={
            'axis': {'range': [None, 2000], 'tickcolor': TEXT_SECONDARY, 'tickfont': {'color': TEXT_SECONDARY}},
            'bar': {'color': gauge_color, 'thickness': 0.8},
            'bgcolor': 'rgba(0,0,0,0)',
            'borderwidth': 2,
            'bordercolor': '#1f1f1f',
            'steps': [
                {'range': [0, 500], 'color': '#141414'},
                {'range': [500, 1000], 'color': '#171717'},
                {'range': [1000, 1500], 'color': '#1a1a1a'},
                {'range': [1500, 2000], 'color': '#1f1f1f'}
            ]
        }
    ))
    
    fig2.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=TEXT_SECONDARY),
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return fig1, fig2, f"{temp:.1f}°C", f"{vib:.1f} mm/s", f"{current_rpm:.0f} RPM", f"{current:.1f} A"

if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=8050)