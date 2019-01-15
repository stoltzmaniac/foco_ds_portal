import quandl
import altair as alt
import pandas as pd

from project.server.config import BaseConfig


quandl.ApiConfig.api_key = BaseConfig.QUANDL_KEY


class QuandlData:

    def __init__(self):
        quandl.ApiConfig.api_key = BaseConfig.QUANDL_KEY

    def daily_close_ticker_request(self, tickers, start_date, end_date) -> pd.DataFrame:
        fields = ['ticker', 'date', 'adj_close']
        data = quandl.get_table('WIKI/PRICES', ticker=tickers,
                                qopts={'columns': fields},
                                date={'gte': start_date, 'lte': end_date},
                                paginate=True)
        data = data.reset_index()[fields]
        return data


class FinancePlots:

    def __init__(self):
        pass

    def multi_line_plot(self, data: pd.DataFrame, x_axis: str, y_axis: str, color: str):
        # Create a selection that chooses the nearest point & selects based on x-value
        nearest = alt.selection(type='single', nearest=True, on='mouseover',
                                fields=[y_axis], empty='none')
        line = alt.Chart().mark_line(interpolate='basis').encode(
            x=f"{x_axis}",
            y=f"{y_axis}",
            color=f"{color}"
        )
        # Transparent selectors across the chart. This is what tells us
        # the x-value of the cursor
        selectors = alt.Chart().mark_point().encode(
            x=f"{x_axis}",
            opacity=alt.value(0),
        ).add_selection(
            nearest
        )
        # Draw points on the line, and highlight based on selection
        points = line.mark_point().encode(
            opacity=alt.condition(nearest, alt.value(1), alt.value(0))
        )
        # Draw text labels near the points, and highlight based on selection
        text = line.mark_text(align='left', dx=5, dy=-5).encode(
            text=alt.condition(nearest, f"{y_axis}", alt.value(' '))
        )
        # Draw a rule at the location of the selection
        rules = alt.Chart().mark_rule(color='gray').encode(
            x=f"{x_axis}",
        ).transform_filter(
            nearest
        )
        # Put the five layers into a chart and bind the data
        plot = alt.layer(line, selectors, points, rules, text,
                         data=data, width=600, height=300)
        return plot
