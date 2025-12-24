import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import random
import time

app = dash.Dash(__name__)

def generate_data():
    return {
        'temperature': random.uniform(60, 85),
        'vibration': random.uniform(1, 5),
        'rpm': random.randint(1200, 1800)
    }

app.layout = html.Div([
    html.H1("Smart Factory Digital Twin - Simple Demo"),
    dcc.Graph(id='live-graph'),
    html.Div(id='status'),
    dcc.Interval(id='interval', interval=1000, n_intervals=0)
])

@app.callback(
    [Output('live-graph', 'figure'), Output('status', 'children')],
    [Input('interval', 'n_intervals')]
)
def update_dashboard(n):
    data = generate_data()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=[data['temperature']], name='Temperature'))
    fig.add_trace(go.Scatter(y=[data['vibration']], name='Vibration'))
    fig.add_trace(go.Scatter(y=[data['rpm']/10], name='RPM/10'))
    
    status = f"Temperature: {data['temperature']:.1f}°C | Vibration: {data['vibration']:.1f} | RPM: {data['rpm']}"
    
    return fig, status

if __name__ == '__main__':
    print("Starting Simple Digital Twin Demo...")
    print("Open browser: http://localhost:8050")
    app.run(debug=True)