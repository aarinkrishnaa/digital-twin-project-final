import plotly.graph_objs as go

def create_sensor_chart(df, metric):
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=df[metric], name=metric))
    return fig