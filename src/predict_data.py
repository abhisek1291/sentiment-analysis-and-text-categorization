#################################
# Author : Abhisek Mohanty
# Description : Reads the Data to be classified from disk and preps it
#################################

try:
    import json
except ImportError:
    import simplejson as json

import diskaccess as da
import country as ct
import pandas as pd

country_trends = dict()
data = pd.DataFrame()
list_country = []
list_trends = []
list_tweets = []


# def preparerealtimedata(country_data, country_name):
#     country_trends[country_name] = list(country_data.keys())
#
#     for key in country_data.keys():
#         for tweet in country_data[key]:
#             list_country.append(country_name)
#             list_trends.append(key)
#         list_tweets.append(tweet)
#
#     data['country'] = list_country
#     data['trend'] = list_trends
#     data['tweet'] = list_tweets
#
#     return data


def preparerealtimedata():
    # print ct.countries
    for name, c_id in ct.countries.iteritems():
        if name != '':
            country_data = da.readFileFromDisk('predict_data', name)
            country_trends[name] = list(country_data.keys())

            for key in country_data.keys():
                for tweet in country_data[key]:
                    list_country.append(name)
                    list_trends.append(key)
                    list_tweets.append(tweet)

    data['country'] = list_country
    data['trend'] = list_trends
    data['tweet'] = list_tweets

    return data
