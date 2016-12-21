#################################
# Author : Abhisek Mohanty
# Description : Gets the Training Data From Twitter and writes to disk
#################################
import re

try:
    import json
except ImportError:
    import simplejson as json

import os
import pandas as pd


def clean_tweet(tweet_row):
    tweet = tweet_row['SentimentText']
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())


def readTrainingDataForSentimentAnalysis():
    subdirectory = 'sentiment_train_data'
    loaded_data = pd.read_csv(
        os.path.join(subdirectory, 'train.csv'),
        # os.path.join(subdirectory, 'Sentiment_Analysis_Dataset.csv'),
        error_bad_lines=False
    )

    loaded_data.columns = ['Sentiment', 'id', 'date', 'query', 'user', 'SentimentText']
    # loaded_data.head()
    final_data = loaded_data
    final_data = loaded_data.groupby('Sentiment').head(50000).reset_index(drop=True)  # Take the first 100,000 rows for training
    final_data.shape

    final_data['tweet'] = final_data.apply(lambda row: clean_tweet(row), axis=1)
    return final_data
