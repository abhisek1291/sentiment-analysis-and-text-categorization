#################################
# Author : Abhisek Mohanty
# Description : Gets the list of countries and the trends.
#################################

try:
    import json
except ImportError:
    import simplejson as json


countries = dict()


def getcountrylist(api_connection):

    # we wouldn't want to miss any countries
    max_iter = 2

    for i in range(0, max_iter):
        trends = api_connection.trends.available(_woeid=1)
        trends_json = json.dumps(trends, indent=5)
        trends_data = json.loads(trends_json)
        for trend in trends_data:
            if not trend['country'] in countries:
                countries[trend['country']] = trend['woeid']

