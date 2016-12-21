#################################
# Author : Abhisek Mohanty
# Description : Create and train sentiment classifier
#################################

try:
    import json
except ImportError:
    import simplejson as json

from sklearn.cross_validation import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
import nltk
import sklearn.metrics as mt
import sklearn.naive_bayes as nb

stopwords = nltk.corpus.stopwords.words('english')

vectorizer = TfidfVectorizer(
    min_df=5,
    max_df=0.8,
    sublinear_tf=True,
    use_idf=True,
    ngram_range=(1,4),
    stop_words=stopwords
)


def vectorize():
    return vectorizer


def trainSVM(train_test_data):
    x_train, x_test, y_train, y_test = train_test_split(
        train_test_data['tweet'],
        train_test_data['Sentiment'],
        test_size=0.1,
        random_state=42
    )

    # Split into validation data as well

    train_vectors = vectorizer.fit_transform(x_train)
    test_vectors = vectorizer.transform(x_test)

    classifier_rbf = svm.SVC(C=2000, kernel='rbf')
    classifier_rbf.fit(train_vectors, y_train)
    prediction_rbf = classifier_rbf.predict(test_vectors.toarray())

    return classifier_rbf


def trainNaiveBayes(train_test_data):
    x_train, x_test, y_train, y_test = train_test_split(
        train_test_data['tweet'],
        train_test_data['Sentiment'],
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
