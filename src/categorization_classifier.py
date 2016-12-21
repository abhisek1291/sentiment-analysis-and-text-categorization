#################################
# Author : Abhisek Mohanty
# Description : Create and train the SVM classifier on the tf-idf vectors
#################################

try:
    import json
except ImportError:
    import simplejson as json

from sklearn.cross_validation import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
import pandas as pd
import sklearn.naive_bayes as nb
import sklearn.metrics as mt

vectorizer = TfidfVectorizer(
    min_df=5,
    max_df=0.8,
    sublinear_tf=True,
    use_idf=True
)


def vectorize():
    return vectorizer


def trainSVM(train_test_data):
    train_data = pd.DataFrame(train_test_data)
    # train_data = train_data.sample(n=10000, random_state=42) ## Remove
    train_data.columns = ['y', 'X']

    x_train, x_test, y_train, y_test = train_test_split(
        train_data['X'],
        train_data['y'],
        test_size=0.1,
        random_state=42
    )

    train_vectors = vectorizer.fit_transform(x_train)
    test_vectors = vectorizer.transform(x_test)

    classifier_rbf = svm.SVC(C=2500)
    classifier_rbf.fit(train_vectors, y_train)
    prediction_rbf = classifier_rbf.predict(test_vectors)

    zipped = zip(prediction_rbf, y_test, x_test)

    errors = 0
    total = 0
    for val in zipped:
        total += 1
        if val[0] != val[1]:
            errors += 1

    print "errors : " + str(errors) + " total : " + str(total)

    return classifier_rbf


def trainNaiveBayes(train_test_data):
    train_data = pd.DataFrame(train_test_data)
    # train_data = train_data.sample(n=10000, random_state=42) ## Remove
    train_data.columns = ['y', 'X']

    x_train, x_test, y_train, y_test = train_test_split(
        train_data['X'],
        train_data['y'],
        test_size=0.1,
        random_state=42
    )

    train_vectors = vectorizer.fit_transform(x_train)
    test_vectors = vectorizer.transform(x_test)

    naive_bayes = nb.MultinomialNB()
    naive_bayes.fit(train_vectors, y_train)
    prediction_nb = naive_bayes.predict(test_vectors)

    cm = mt.confusion_matrix(y_test, prediction_nb)
    # print cm
    # print mt.accuracy_score(y_test, prediction_nb)

    return naive_bayes
