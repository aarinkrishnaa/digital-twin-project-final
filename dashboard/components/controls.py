from dash import dcc, html

def create_control_panel():
    return html.Div([
        dcc.Slider(id='interval-slider', min=1, max=10, value=2)
    ])