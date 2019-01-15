import datetime as dt

import pytest

from project.server.user.models import User, Role
from project.server.twitter.utils import TwitterData, twtr
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
