#######################################
#
# author : Abhisek Mohanty
# description : Generates the document term matrix for the tweets after generating its tf-idf values.
#
#######################################

import nltk, math, re, os, json
from collections import OrderedDict
import concept_class as cc


def getconceptclass(category):
    return str(cc.getconceptclass(category))


def freq(word, tokens):
    return tokens.count(word)


def freq(word, doc):
    return doc.count(word)


def word_count(doc):
    return len(doc)


def tf(word, doc):
    return freq(word, doc) / float(word_count(doc))


def num_docs_containing(word, list_of_docs):
    count = 0
    for document in list_of_docs:
        if freq(word, document) > 0:
            count += 1
    return 1 + count


def idf(word, list_of_docs):
    return math.log(len(list_of_docs) /
                    float(num_docs_containing(word, list_of_docs)))


def tf_idf(word, doc, list_of_docs):
    return tf(word, doc) * idf(word, list_of_docs)


def create_document_term_matrix():
    vocabulary = dict()
    docs = dict()
    stopwords = nltk.corpus.stopwords.words('english')
    tokenizer = nltk.tokenize.RegexpTokenizer("[\w’]+", flags=re.UNICODE)
    train_data = []

    subdirectory = 'train_data'
    categories = list(cc.categories_keys.keys())

    for category in categories:
        with open(os.path.join(subdirectory, '%s.json' % category), 'r') as data_file:
            data = json.load(data_file)

        for tweet in (data['tweets']):
            tokens = tokenizer.tokenize(tweet)

            tokens = [token.lower() for token in tokens if len(token) > 2]
            tokens = [token for token in tokens if token not in stopwords]

            final_tokens = tokens

            for token in final_tokens:
                if token in vocabulary:
                    vocabulary[token] += 1
                else:
                    vocabulary[token] = 1

            docs[tweet] = {'category': category, 'freq': {}, 'tf': {}, 'idf': {},
                           'tf-idf': {}, 'tokens': []}

            for token in final_tokens:
                # The frequency computed for each tip
                docs[tweet]['freq'][token] = freq(token, final_tokens)
                # The term-frequency (Normalized Frequency)
                docs[tweet]['tf'][token] = tf(token, final_tokens)
                docs[tweet]['tokens'] = final_tokens

    vocabulary_ordered_dict = OrderedDict(sorted(vocabulary.items(), key=lambda t: t[0]))
    with open(os.path.join(subdirectory, 'vocabulary.txt'), 'w') as f:
        for key in vocabulary_ordered_dict:
            print >> f, key

    for doc in docs:
        if doc != '':
            for token in docs[doc]['tf']:
                # The Inverse-Document-Frequency
                docs[doc]['idf'][token] = idf(token, vocabulary)
                # The tf-idf
                docs[doc]['tf-idf'][token] = tf_idf(token, docs[doc]['tokens'], vocabulary)

            data = docs[doc]

            datafile_line = []
            tf_idfs = data['tf-idf']
            datafile_line.append(
                getconceptclass(data['category']))  # Call a method which returns the corresponding Concept Class

            for token in data['tokens']:
                line_number = vocabulary_ordered_dict.keys().index(token) + 1  # manage a way to use the dictionary
                datafile_line.append(str(line_number) + ':' + str(tf_idfs[token]))

            with open(os.path.join(subdirectory, 'data.txt'), 'a') as f:
                f.write(" ".join(datafile_line) + '\n')

            train_data.append(datafile_line)
    return train_data
