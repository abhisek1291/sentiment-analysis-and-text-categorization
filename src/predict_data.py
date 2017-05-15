#################################
# Author : Abhisek Mohanty
# Description : Reads the Data to be classified from disk and preps it
#               This realtime data (which is to be classified) is already fetched from twitter previously
#               using the tweets.py file.
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


def preparerealtimedata():
    '''
    Returns the realtime data which needs to be classified.
    '''
    
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
