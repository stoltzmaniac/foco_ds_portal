import time
from collections import namedtuple
from urllib.parse import quote_plus

from flask import jsonify

from project.server.utils import twtr


def twitter_search(request) -> list:
    form_data = request.form
    search_query = (
        f"q={quote_plus(form_data['search_term'])}&count={str(form_data['count'])}"
    )
    results = twtr.GetSearch(raw_query=search_query)
    data = []
    for r in results:
        d = r.AsDict()
        d["timestamp"] = time.strftime(
            "%Y-%m-%d %H:%M:%S",
            time.strptime(d["created_at"], "%a %b %d %H:%M:%S +0000 %Y"),
        )
        data.append(d)
    return data


def twitter_timeline(request) -> list:
    form_data = request.form
    results = twtr.GetUserTimeline(screen_name=form_data['username'], count=1000)
    data = [i.text for i in results]
    return data


def twitter_timeline2(screen_name) -> list:
    results = twtr.GetUserTimeline(screen_name=screen_name, count=1000)
    data = [i.text for i in results]
    return data


def twitter_congressional_list():
    r_house = [dict(i.AsDict(), chamber='house_of_representatives', party='republican') for i in twtr.GetListMembers(slug='house-republicans', owner_screen_name='HouseGOP')]
    d_house = [dict(i.AsDict(), chamber='house_of_representatives', party='democrat') for i in twtr.GetListMembers(slug='house-democrats', owner_screen_name='HouseDemocrats')]
    r_senate = [dict(i.AsDict(), chamber='senate', party='republican') for i in twtr.GetListMembers(slug='senaterepublicans', owner_screen_name='SenateGOP')]
    d_senate = [dict(i.AsDict(), chamber='senate', party='democrat') for i in twtr.GetListMembers(slug='senatedemocrats', owner_screen_name='SenateDems')]
    congress = r_house + d_house + r_senate + d_senate
    return congress




