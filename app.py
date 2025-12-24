import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import random

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1("Smart Factory Digital Twin - Demo", 
           style={'textAlign': 'center', 'color': '#ffffff', 'backgroundColor': '#141414', 'padding': '20px', 'margin': '0'}),
    
    html.Div([
        html.Button("Start Motor", id='start-btn', n_clicks=0, 
                   style={'backgroundColor': '#10b981', 'color': 'white', 'padding': '10px 20px', 'margin': '10px', 'border': 'none', 'borderRadius': '5px'}),
        html.Button("Stop Motor", id='stop-btn', n_clicks=0,
                   style={'backgroundColor': '#ef4444', 'color': 'white', 'padding': '10px 20px', 'margin': '10px', 'border': 'none', 'borderRadius': '5px'}),
        html.Div(id='status', style={'color': '#ffffff', 'fontSize': '18px', 'margin': '20px'})
    ], style={'backgroundColor': '#141414', 'padding': '20px', 'margin': '20px', 'borderRadius': '8px'}),
    
    html.Div([
        html.Div([
            html.H3("Temperature", style={'color': '#ffffff'}),
            html.Div(id='temp', style={'color': '#ef4444', 'fontSize': '24px'})
        ], style={'backgroundColor': '#141414', 'padding': '20px', 'margin': '10px', 'borderRadius': '8px', 'flex': '1'}),
        
        html.Div([
            html.H3("RPM", style={'color': '#ffffff'}),
            html.Div(id='rpm', style={'color': '#10b981', 'fontSize': '24px'})
        ], style={'backgroundColor': '#141414', 'padding': '20px', 'margin': '10px', 'borderRadius': '8px', 'flex': '1'})
    ], style={'display': 'flex'}),
    
    dcc.Graph(id='chart'),
    dcc.Interval(id='interval', interval=3000, n_intervals=0)
], style={'backgroundColor': '#0a0a0a', 'minHeight': '100vh', 'fontFamily': 'Arial'})

@app.callback(
    [Output('status', 'children'),
     Output('temp', 'children'),
     Output('rpm', 'children'),
     Output('chart', 'figure')],
    [Input('start-btn', 'n_clicks'),
     Input('stop-btn', 'n_clicks'),
     Input('interval', 'n_intervals')]
)
def update_dashboard(start_clicks, stop_clicks, n):
    ctx = dash.callback_context
    
    # Determine motor state
    running = False
    if ctx.triggered:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if button_id == 'start-btn' and start_clicks > stop_clicks:
            running = True
        elif button_id == 'stop-btn' and stop_clicks >= start_clicks:
            running = False
    
    # Generate data based on state
    if running:
        temp = 70 + random.randint(-10, 10)
        rpm_val = 1500 + random.randint(-100, 100)
        status = "🟢 Motor Running"
    else:
        temp = 22
        rpm_val = 0
        status = "🔴 Motor Stopped"
    
    # Create chart
    x_data = list(range(20))
    y_data = [temp + random.randint(-5, 5) for _ in range(20)]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_data, y=y_data, name='Temperature', line=dict(color='#ef4444')))
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='#141414',
        font=dict(color='#ffffff'),
        title="Sensor Data"
    )
    
    return status, f"{temp}°C", f"{rpm_val} RPM", fig

if __name__ == '__main__':
    app.run_server(debug=False)