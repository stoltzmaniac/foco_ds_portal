import quandl
import pandas as pd
from plotly.offline import plot
import plotly.graph_objs as go

from project.server.config import BaseConfig


quandl.ApiConfig.api_key = BaseConfig.QUANDL_KEY


class QuandlData:
    def __init__(self):
        quandl.ApiConfig.api_key = BaseConfig.QUANDL_KEY

    def daily_close_ticker_request(self, tickers, start_date, end_date) -> pd.DataFrame:
        fields = ["ticker", "date", "adj_close"]
        data = quandl.get_table(
            "WIKI/PRICES",
            ticker=tickers,
            qopts={"columns": fields},
            date={"gte": start_date, "lte": end_date},
            paginate=True,
        )
        data = data.reset_index()[fields]
        return data


class FinancePlots:
    def __init__(self):
        pass

    def line_plot(
        self, data: pd.DataFrame, x_axis: str, y_axis: str, color: str
    ) -> plot:
        dfs = [
            go.Scatter(
                x=data[data[color] == i][x_axis],
                y=data[data[color] == i][y_axis],
                name=i,
            )
            for i in data[color].unique()
        ]
        return plot(dfs, output_type="div", include_plotlyjs=True)
