from dash import html, dcc

def create_main_layout():
    return html.Div([
        html.H1("Digital Twin Dashboard"),
        dcc.Graph(id='main-chart'),
        dcc.Interval(id='interval', interval=2000)
    ])