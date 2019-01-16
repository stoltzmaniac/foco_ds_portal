import datetime as dt

import pytest
import quandl
import pandas as pd
from plotly.offline import plot

from project.server.user.models import User, Role
from project.server.config import BaseConfig
from project.server.twitter.utils import TwitterData, twtr
from project.server.finance.utils import QuandlData, FinancePlots
from .factories import UserFactory


class TestApiTwitter:
    """Twitter API tests."""

    def test_auth(self):
        """Test Twitter Auth by using GetTimeline request as a proxy for no auth endpoint"""
        screen_name = 'stoltzmaniac'
        response = twtr.GetUserTimeline(screen_name=screen_name)
        assert len(response) > 1
        assert response[0].user.screen_name == screen_name
        assert response[0].source == '<a href="http://twitter.com" rel="nofollow">Twitter Web Client</a>'

    def test_timeline_request(self):
        """Test twitter get  user timeline data"""
        yesterday = dt.datetime.now() - dt.timedelta(1)
        screen_name = 'stoltzmaniac'
        tweetr = TwitterData()
        data = tweetr.timeline_request(screen_name=screen_name)
        assert type(data) == list
        assert len(data) > 1
        assert type(data[0]) == dict
        assert data[0]['user']['screen_name'] == screen_name
        assert type(data[0]['text']) == str

    def test_get_search_request(self):
        """Test twitter get  user timeline data"""
        # Assumes people would tweet about 'love' more than 10 times in the last 24 hours
        yesterday = dt.datetime.now() - dt.timedelta(1)
        tweetr = TwitterData()
        data = tweetr.search_request(search_term='love')
        assert type(data) == list
        assert len(data) > 10
        assert type(data[0]) == dict
        assert yesterday < dt.datetime.strptime(data[0]['timestamp'], "%Y-%m-%d %H:%M:%S")
        assert type(data[0]['text']) == str

    def test_list_members_request(self):
        """Test twitter get  user timeline data"""
        yesterday = dt.datetime.now() - dt.timedelta(1)
        tweetr = TwitterData()
        data = tweetr.list_members_request(slug='astronauts', owner_screen_name='NASA')
        assert type(data) == list
        assert len(data) > 1
        assert type(data[0]) == dict
        assert type(data[0]['screen_name']) == str


class TestQuandlApi:
    """Quandl API tests"""

    def test_get_table(self):
        fields = ['ticker', 'date', 'adj_close']
        tickers = ['AAPL', 'MSFT']
        start_date = '2015-01-01'
        end_date = '2016-01-01'
        quandl.ApiConfig.api_key = BaseConfig.QUANDL_KEY
        data = quandl.get_table('WIKI/PRICES', ticker=tickers,
                                qopts={'columns': fields},
                                date={'gte': start_date, 'lte': end_date},
                                paginate=True)
        assert type(data) == pd.DataFrame
        assert sorted(data.columns.tolist()) == sorted(fields)
        assert sorted(data['ticker'].unique().tolist()) == sorted(tickers)

    def test_quandl_data_daily_close_ticker_request(self):
        qd = QuandlData()
        symbols = ['AAPL', 'MSFT']
        fields = ['ticker', 'date', 'adj_close']
        start_date = '2015-01-01'
        end_date = '2016-01-01'
        data = qd.daily_close_ticker_request(symbols, start_date, end_date)
        assert type(data) == pd.DataFrame
        assert sorted(data.columns.tolist()) == sorted(fields)
        assert sorted(data['ticker'].unique().tolist()) == sorted(symbols)

    def test_plot_tickers_over_time(self):
        qd = QuandlData()
        fp = FinancePlots()
        symbols = ['AAPL', 'MSFT']
        start_date = '2015-01-01'
        end_date = '2016-01-01'
        data = qd.daily_close_ticker_request(symbols, start_date, end_date)
        plot = fp.line_plot(data, x_axis='date', y_axis='adj_close', color='ticker')
        assert type(plot) == str
        assert '<div><script type="text/javascript">window.PlotlyConfig' in plot
