import quandl
import altair as alt
import pandas as pd

from project.server.config import BaseConfig


quandl.ApiConfig.api_key = BaseConfig.QUANDL_KEY


def plot_line(data: pd.DataFrame) -> alt.Chart:
    base = alt.Chart(data)
    # Build chart
    line = base.mark_line().encode(
        x='date',
        y='adj_close'
    )
    return line
