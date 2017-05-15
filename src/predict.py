#################################
# Author : Abhisek Mohanty
# Description : Predict the classes of the tweets
#################################

import categorization_classifier as tc
import sentiment_classifier as sc
import concept_class as cc


def predictConceptClass(classifier, data):
    '''
    Predicts the Category of each tweet
    '''
    data_vector = tc.vectorize().transform(data['tweet'])
    prediction_rbf = classifier.predict(data_vector)

    predict_values = prediction_rbf
    predict_values = [cc.getCategoryForClass(int(x)) for x in predict_values]

    # zipped = zip(data['country'], data['trend'], data['tweet'], predict_values)
    # for val in zipped:
    #     print val
    data['class'] = predict_values
    return data


def sentimentForClass(cclass):
    if cclass == 4:
        return 'positive'
    elif cclass == 0:
        return 'negative'
    else:
        return 'neutral'


def predictSentiment(classifier, data):
    '''
    Predicts the sentiment of each tweet.
    '''
    data_vector = sc.vectorize().transform(data['tweet'])
    sentiment_predict = classifier.predict(data_vector)

    sentiment_values = sentiment_predict
    sentiment_values = [sentimentForClass(int(x)) for x in sentiment_values]

    # zipped = zip(data['country'], data['trend'], data['tweet'], predict_values)
    # for val in zipped:
    #     print val
    data['sentiment'] = sentiment_values
    return data
