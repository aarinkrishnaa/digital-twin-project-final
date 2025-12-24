import dash
from dash import dcc, html, Input, Output, dash_table
import plotly.graph_objs as go
import pandas as pd
import random
import numpy as np
import json

app = dash.Dash(__name__)

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
    html.H1("Smart Factory Digital Twin", 
           style={'color': TEXT_PRIMARY, 'textAlign': 'center', 'background': 'linear-gradient(135deg, #141414 0%, #1a1a1a 100%)', 'padding': '40px', 'margin': '0', 'fontSize': '32px', 'fontWeight': '300', 'letterSpacing': '1px', 'borderBottom': '1px solid #1f1f1f'}),
    
    # Motor Control Panel
    html.Div([
        html.H3("Motor Control", style={'color': TEXT_PRIMARY, 'marginBottom': '24px', 'fontSize': '18px', 'fontWeight': '500'}),
        html.Div([
            html.Button("Start", id='start-btn', n_clicks=0, 
                       style={'background': ACCENT_GREEN, 'color': 'white', 'padding': '12px 24px', 'margin': '0 8px', 'border': 'none', 'borderRadius': '6px', 'fontSize': '14px', 'cursor': 'pointer', 'fontWeight': '500', 'transition': 'all 0.2s'}),
            html.Button("Stop", id='stop-btn', n_clicks=0,
                       style={'background': ACCENT_RED, 'color': 'white', 'padding': '12px 24px', 'margin': '0 8px', 'border': 'none', 'borderRadius': '6px', 'fontSize': '14px', 'cursor': 'pointer', 'fontWeight': '500', 'transition': 'all 0.2s'})
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
    
    # Charts Row
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
    
    # 3D Model and Data
    html.Div([
        html.Div([
            html.H3("3D Machine Model", style={'color': TEXT_PRIMARY, 'marginBottom': '20px', 'fontSize': '18px', 'fontWeight': '500'}),
            html.Iframe(id='3d-iframe', src='/assets/3d.html', style={'width': '100%', 'height': '500px', 'border': 'none', 'borderRadius': '8px'})
        ], style={'background': CARD_BG, 'padding': '24px', 'margin': '12px', 'borderRadius': '8px', 'flex': '2', 'border': '1px solid #1f1f1f'}),
        
        html.Div([
            html.H3("Machine Status", style={'color': TEXT_PRIMARY, 'marginBottom': '20px', 'fontSize': '18px', 'fontWeight': '500'}),
            html.Div(id='machine-status', style={'color': TEXT_SECONDARY, 'fontSize': '14px'})
        ], style={'background': CARD_BG, 'padding': '24px', 'margin': '12px', 'borderRadius': '8px', 'flex': '1', 'border': '1px solid #1f1f1f'})
    ], style={'display': 'flex', 'padding': '0 12px'}),
    
    # Data Table
    html.Div([
        html.H3("Recent Data Points", style={'color': TEXT_PRIMARY, 'marginBottom': '20px', 'fontSize': '18px', 'fontWeight': '500'}),
        html.Div(id='data-table')
    ], style={'background': CARD_BG, 'padding': '24px', 'margin': '24px', 'borderRadius': '8px', 'border': '1px solid #1f1f1f'}),
    
    dcc.Interval(id='interval', interval=1000, n_intervals=0)
], style={'fontFamily': 'Inter, -apple-system, BlinkMacSystemFont, sans-serif', 'background': DARK_BG, 'minHeight': '100vh'})

# Motor control callback
@app.callback(
    [Output('motor-status', 'children'),
     Output('3d-iframe', 'src')],
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
        
        # Write state for 3D model
        try:
            with open('motor_state.json', 'w') as f:
                json.dump({'running': motor_running, 'target_rpm': target_rpm}, f)
        except:
            pass
    
    status = f"🟢 Motor Running - Target: {target_rpm} RPM" if motor_running else f"🔴 Motor Stopped - Target: {target_rpm} RPM"
    
    # Update 3D model via URL parameters
    iframe_src = f'/assets/3d.html?running={str(motor_running).lower()}&rpm={target_rpm}&t={random.randint(1,1000)}'
    
    return status, iframe_src

# Dashboard updates
@app.callback(
    [Output('trends-chart', 'figure'),
     Output('rpm-gauge', 'figure'),
     Output('temp-display', 'children'),
     Output('vib-display', 'children'),
     Output('rpm-display', 'children'),
     Output('current-display', 'children'),
     Output('machine-status', 'children'),
     Output('data-table', 'children')],
    [Input('interval', 'n_intervals')]
)
def update_dashboard(n):
    global motor_running, target_rpm
    
    if motor_running:
        # MOTOR RUNNING - Generate active data
        current_rpm = target_rpm + random.randint(-50, 50)
        temp = 70 + random.randint(-10, 10)
        vib = 3.5 + random.uniform(-1, 1)
        current = 12 + random.uniform(-2, 2)
        
        # Active trend data
        trend_data = pd.DataFrame({
            'temp': np.random.normal(temp, 3, 50),
            'vib': np.random.normal(vib, 0.5, 50),
            'current': np.random.normal(current, 1, 50)
        })
        
        line_style = dict(width=3)
        
    else:
        # MOTOR STOPPED - Everything at zero/ambient
        current_rpm = 0
        temp = 22  # Ambient
        vib = 0.0  # No vibration
        current = 0.0  # No current
        
        # Flat line data
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
            ],
            'threshold': {
                'line': {'color': ACCENT_RED, 'width': 4},
                'thickness': 0.75,
                'value': 1900
            }
        }
    ))
    
    fig2.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=TEXT_SECONDARY),
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    # Machine Status
    power_status = "Online" if motor_running else "Standby"
    power_color = ACCENT_GREEN if motor_running else ACCENT_ORANGE
    
    status_panel = html.Div([
        html.Div([
            html.H4("Power Status", style={'color': TEXT_PRIMARY, 'fontSize': '14px', 'margin': '0 0 8px 0', 'fontWeight': '500'}),
            html.P(power_status, style={'color': power_color, 'fontSize': '12px', 'margin': '0'})
        ], style={'marginBottom': '16px', 'paddingBottom': '16px', 'borderBottom': '1px solid #1f1f1f'}),
        
        html.Div([
            html.H4("Temperature", style={'color': TEXT_PRIMARY, 'fontSize': '14px', 'margin': '0 0 8px 0', 'fontWeight': '500'}),
            html.P(f"Current: {temp:.1f}°C", style={'color': TEXT_SECONDARY, 'fontSize': '12px', 'margin': '0'}),
            html.P(f"Status: {'Normal' if temp < 80 else 'High'}", 
                  style={'color': ACCENT_GREEN if temp < 80 else ACCENT_RED, 'fontSize': '12px', 'margin': '4px 0 0 0'})
        ], style={'marginBottom': '16px', 'paddingBottom': '16px', 'borderBottom': '1px solid #1f1f1f'}),
        
        html.Div([
            html.H4("Motor", style={'color': TEXT_PRIMARY, 'fontSize': '14px', 'margin': '0 0 8px 0', 'fontWeight': '500'}),
            html.P(f"RPM: {current_rpm:.0f}", style={'color': TEXT_SECONDARY, 'fontSize': '12px', 'margin': '0'}),
            html.P(f"Current: {current:.1f}A", style={'color': TEXT_SECONDARY, 'fontSize': '12px', 'margin': '0'}),
            html.P(f"Status: {'Running' if current_rpm > 0 else 'Stopped'}", 
                  style={'color': ACCENT_GREEN if current_rpm > 0 else ACCENT_RED, 'fontSize': '12px', 'margin': '4px 0 0 0'})
        ])
    ])
    
    # Data Table
    table_data = pd.DataFrame({
        'timestamp': [f"2024-01-01 12:{i:02d}:00" for i in range(10)],
        'temperature': [temp + random.uniform(-2, 2) for _ in range(10)],
        'vibration': [vib + random.uniform(-0.5, 0.5) for _ in range(10)],
        'rpm': [current_rpm] * 10,
        'current': [current + random.uniform(-1, 1) for _ in range(10)]
    })
    
    table = dash_table.DataTable(
        data=table_data.round(2).to_dict('records'),
        columns=[{"name": i.title(), "id": i} for i in table_data.columns],
        style_cell={
            'textAlign': 'center', 
            'fontSize': '12px',
            'color': TEXT_PRIMARY,
            'backgroundColor': CARD_BG,
            'border': '1px solid #1f1f1f',
            'padding': '12px'
        },
        style_header={
            'backgroundColor': '#1f1f1f', 
            'color': TEXT_PRIMARY, 
            'fontWeight': '500',
            'border': '1px solid #1f1f1f'
        }
    )
    
    return fig1, fig2, f"{temp:.1f}°C", f"{vib:.1f} mm/s", f"{current_rpm:.0f} RPM", f"{current:.1f} A", status_panel, table

# Export server for Vercel
server = app.server

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)