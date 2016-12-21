#################################
# Author : Abhisek Mohanty
# Description : Gets the Training Data for Text Categorization Task From Twitter and writes to disk
# 5-6 selected twitter accounts for each category
# Since twitter limits number of api calls per 15 mins, we put the application to sleep 
# once the number is exhausted and resume after 15 minutes.
#################################

try:
    import json
except ImportError:
    import simplejson as json

import re
import time
from datetime import datetime

import diskaccess as wtd

user_names_by_categories = {
    'sports': ['espn', 'ESPNcricinfo', 'BBCSport', 'FOXSports', 'NBCSports'],
    'tech': ['engadget', 'TechCrunch', 'techreview', 'ForbesTech', 'Pocketnow'],
    'travel': ['lonelyplanet', 'SmarterTravel', 'NatGeo', 'TravelEditor', 'BudgetTravel', 'TravelIndustry'],
    'food': ['nytfood', 'grubstreet', 'epicurious', 'WholeFoods', 'Starbucks', 'foodandwine'],
    'politics': ['CNNPolitics', 'nytpolitics', 'ABCPolitics', 'postpolitics', 'ETPolitics', 'ReutersPolitics',
                 'ReutersPolitics'],
    'automobiles': ['autocar', 'automobilemag', 'AutoExpress', 'MotorTrend', 'chevrolet', 'CARmagazine'],
    'weather': ['weatherchannel', 'breakingweather', 'wunderground', 'bbcweather', 'WeatherBug', 'accuweather'],
    'music': ['RollingStone', 'Spotify', 'TeleMusicNews', 'guardianmusic', 'MTVMusicUK', 'BBC6Music', 'AppleMusic'],
    'entertainment': ['IMDb', 'RottenTomatoes', 'EW', 'eonline', 'etnow', 'ParamountPics'],
    'business': ['HarvardBiz', 'nytimesbusiness', 'WSJ', 'NBCNewsBusiness', 'EconomicTimes', 'businessinsider'],
    'shopping': ['NYCShopGuide', 'amazondeals', 'Flipkart', 'slickdeals', 'DealsPlus', 'KicksDeals'],
    'science': ['ScienceNews', 'NewsfromScience', 'sciencemagazine', 'sciam', 'newscientist', 'scicurious'],
    'health': ['goodhealth', 'MensHealthMag', 'WomensHealthMag', 'HarvardHealth', 'NYTHealth', 'cnnhealth'],
    'property': ['TeleProperty', 'PropertyWire', 'PWNews', 'EstatesGazette', 'TimesProperty', 'ETRealEstate', 'PropertyTalk']
}

TWEET_SLEEP_TIMER = 930
number_of_api_calls = 0


def textfromtweets(all_tweets):
    tweets_list = []
    for tweet in all_tweets:
        tweets_list.append(
            ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet['text']).split()))
    return tweets_list


def gettrainingdata(api_connection, category):

    # Travel tweets are low in number. 7k Set the tweets count accordingly

    global number_of_api_calls
    max_id = 0
    max_api_calls = 20  # maximum can be 300, but maximum let have it at 100
    tweet_count_per_user = 200
    tweets_from_user = []

    for user_name in user_names_by_categories[category]:
        print '\nGetting data for username : ' + user_name
        with_max_id = False
        if number_of_api_calls > 150:
            print '\nAPI Calls > 89. Wouldnt want to risk termination. Sleeping for 15:30 mins'
            print 'Starting at ' + str(datetime.now().strftime('%H:%M:%S'))
            time.sleep(TWEET_SLEEP_TIMER)
            number_of_api_calls = 0  ## Reset number of API Calls and start again
            print '\nStarting Tweet Retrieval Again'

        for i in range(0, max_api_calls):
            print '     API Call #' + str(i)
            if with_max_id == False:
                tweets = api_connection.statuses.user_timeline(screen_name=user_name, count=tweet_count_per_user)
                number_of_api_calls += 1
            else:
                tweets = api_connection.statuses.user_timeline(screen_name=user_name, count=tweet_count_per_user, max_id=max_id)
                number_of_api_calls += 1

            if not tweets:
                print 'No More Tweets. Break...'
                break

            tweets_from_user.append(textfromtweets(tweets))
            number_of_tweets_retrieved = len(tweets)
            max_id = tweets[number_of_tweets_retrieved - 1]['id']  # get the max id from the last tweet from the batch -> tweet no. 199
            with_max_id = True

    flattened_list_of_tweets = [y for x in tweets_from_user for y in x]
    tweets_dict = {'category': category, 'tweets': flattened_list_of_tweets}
    print '\nWriting data for category : ' + category + ' to DISK.'
    wtd.generateFile(tweets_dict, 'train_data', category, 'w')

