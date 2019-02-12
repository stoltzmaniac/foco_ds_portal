import pandas as pd
from plotly.offline import plot
import plotly.graph_objs as go



class BasicPlot:
    """Plotting 'library' """

    def __init__(self):
        pass

    def line(self, data: pd.DataFrame, x_axis: str, y_axis: str, color: str) -> plot:
        line = go.Scatter(
            x=data[x_axis],
            y=data[y_axis],
            mode='lines',
            marker=dict(color=color))
        return line

    def scatter(self, data: pd.DataFrame, x_axis: str, y_axis: str, color: str) -> plot:
        scatter = go.Scatter(
            x=data[x_axis],
            y=data[y_axis],
            name=x_axis + " vs. " + y_axis,
            mode='markers',
            marker=dict(color=color))
        return scatter

    @staticmethod
    def plot_to_div(plot_obj_list):
        return plot(plot_obj_list, output_type='div', include_plotlyjs=True)
