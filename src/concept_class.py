#################################
# Author : Abhisek Mohanty
# Description : The list of Concept Classes for the categorization part
#################################

categories_keys = {
    'sports': 0,
    'tech': 1,
    'travel': 2,
    'food': 3,
    'politics': 4,
    'automobiles': 5,
    'weather': 6,
    'music': 7,
    'entertainment': 8,
    'business': 9,
    'shopping': 10,
    'science': 11,
    'health': 12,
    'property': 13
}

keys_categories = dict((v, k) for k, v in categories_keys.iteritems())


def getconceptclass(category):
    return str(categories_keys[category])


def getCategoryForClass(cclass):
    return keys_categories[cclass]
