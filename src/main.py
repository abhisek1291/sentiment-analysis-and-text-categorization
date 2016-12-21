#################################
# Author : Abhisek Mohanty
# Description :
#################################

from twitter import Twitter, OAuth
import tweets
import categorization_training_data as td
import predict_data as pd
import country as ct
import concept_class as cc
import categorization_classifier as catcls
import categorization_process_traindata as cpt
import sentiment_training_data as std
import sentiment_classifier as sc
import predict as pdt
import cPickle
import warnings
warnings.filterwarnings("ignore")

# Variables that contains the user credentials to access Twitter API
ACCESS_TOKEN = 'ENTER_ACCESS_TOKEN_HERE'
ACCESS_SECRET = 'ENTER_ACCESS_SECRET_HERE'
CONSUMER_KEY = 'ENTER_CONSUMER_KEY_HERE'
CONSUMER_SECRET = 'ENTER_CONSUMER_SECRET_HERE'

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

# Initiate the connection to Twitter Streaming API
connection = Twitter(auth=oauth)

print 'starting....'
print '\nbrace yourself for the next few hours'

print '\nget country data'
ct.getcountrylist(connection)

# Get Training Data
categories = list(cc.categories_keys.keys())

# get tweets for training the categorization classifier.
# the 2 lines below need to be uncommented for getting the latest data
# note : this takes long as twitter limits accesses to 180 every 15 mins
# and 200 tweets per access

# print 'get country data'
print '\nalready fetched training data. takes about 6-7 hours to fetch real time training data from twitter'
for category in categories:
    td.gettrainingdata(connection, category)

# train classifiers

print '\nprepare categorization training data'
categorization_train_data = cpt.preparetraindata(categories)
# print '\n'.join(str(p) for p in categorization_train_data[0:10])

print '\ntraining categorization classifier'
categorization_classifier = catcls.trainSVM(categorization_train_data)
nb_categorization_classifier = catcls.trainNaiveBayes(categorization_train_data)
print '\ncategorization classifier training done'

print '\nprepare sentiment training data'
sentiment_train_data = std.readTrainingDataForSentimentAnalysis()

print '\ntraining sentiment classifier'
sentiment_classifier = sc.trainSVM(sentiment_train_data)
nb_sentiment_classifier = sc.trainNaiveBayes(sentiment_train_data)
print '\nsentiment classifier training done'

print '\nwriting classifier to disk'
# save the classifier
with open('sentiment_classifier.pkl', 'wb') as fid:
    cPickle.dump(sentiment_classifier, fid)

# print '\nretrieving classifier from disk'
# with open('sentiment_classifier.pkl', 'rb') as fid:
#     sentiment_classifier = cPickle.load(fid)

# get tweets to be classified and run sentiment analysis on
# input("Waiting...Press Enter to continue...")

print '\nretrieve real time tweets from twitter for categorization and sentiment analysis'
real_time_data = tweets.retrievetweets(connection) # takes very long
print '\nreal time data fetch done'

# run classifiers on realtime data

print '\nprepare real time data'
real_time_data = pd.preparerealtimedata()
# print real_time_data.head(-10)

# categorization classifier

print '\nstarting prediction'
svm_predicted_data = pdt.predictConceptClass(categorization_classifier, real_time_data)
svm_predicted_data = pdt.predictSentiment(sentiment_classifier, real_time_data)

nb_predicted_data = pdt.predictConceptClass(nb_categorization_classifier, real_time_data)
nb_predicted_data = pdt.predictSentiment(nb_sentiment_classifier, real_time_data)

# writing the final prediction file to disk

print '\nwriting predicted data to disk'
nb_predicted_data.to_csv('prediction/output_main_nb.csv', encoding='utf-8')
svm_predicted_data.to_csv('prediction/output_main_svm.csv', encoding='utf-8')
