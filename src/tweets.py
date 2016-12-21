#################################
# Author : Abhisek Mohanty
# Description :
#################################
import re

try:
    import json
except ImportError:
    import simplejson as json

import country as ct
import time
import diskaccess as da
import predict_data as pdt
import pandas as pd
from datetime import datetime

TWITTER_SLEEP_TIME = 930.0
real_time_data = pd.DataFrame()


def textfromtweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())


def retrievetweets(api_connection):
    global real_time_data
    # country_ids = ct.getcountrylist(api_connection)
    country_ids = ct.countries

    while True:
        print '\nwhile iteration #'
        if not bool(country_ids):
            break
        else:
            missed_countries = dict()
            for name, country_id in country_ids.items():
                print '\n' + name
                country_ids.pop(name, None)
                try:
                    if name != '':
                        tweets_by_topic_country = fetch_tweets_from_twitter_api(api_connection, country_id)
                        if bool(tweets_by_topic_country):
                            # tweets_by_topic_country['country'] = name  ## We dont need to do this
                            da.generateFile(tweets_by_topic_country, 'predict_data', name, 'w')
                            # real_time_data = real_time_data.append(pdt.preparerealtimedata(tweets_by_topic_country, name))

                except Exception as ex:
                    if 'Rate limit exceeded' in ex.message:
                        if name not in missed_countries:
                            missed_countries[name] = country_id
                            # timer logic
                        print 'Rate Limit Exceeded. Sleeping for 15:30 mins'
                        print 'Starting at ' + str(datetime.now().strftime('%H:%M:%S'))
                        time.sleep(TWITTER_SLEEP_TIME)
                        print 'Waking for next iteration'
                        continue

        country_ids.clear()
        print 'missed countries'
        print missed_countries
        country_ids = missed_countries
    return real_time_data


def fetch_tweets_from_twitter_api(api_connection, country_id):
    india_trends = api_connection.trends.place(_id=country_id)

    trending_topics = []
    topic_tweets = dict()

    # Change this to a larger number later
    tweets_per_topic = 50

    json_data = json.dumps(india_trends)
    j_data = json.loads(json_data)
    for trend in j_data[0]["trends"]:
        trending_topics.append(trend['query'])

    # Get the tweets for each trending topic
    # Logic for each country
    # country_ids contain the list of countries

    for topic in trending_topics:
        tweets = api_connection.search.tweets(q=topic, lang='en', count=tweets_per_topic)
        for tweet in tweets["statuses"]:
            if topic in topic_tweets:
                topic_tweets[topic].append(textfromtweet(tweet["text"]))  # Need to check min number of words
            else:
                topic_tweets[topic] = [tweet["text"]]

    return topic_tweets
