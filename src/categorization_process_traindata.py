#################################
# Author : Abhisek Mohanty
# Description : Reads Training Data From disk and preps it for the SVM
#################################

try:
    import json
except ImportError:
    import simplejson as json

import concept_class as cc
import diskaccess as da

subdirectory = 'train_data'


def preparetraindata(categories):
    data_file = []
    for category in categories:
        json_data = da.readFileFromDisk(subdirectory, category)

        y_label = cc.getconceptclass(category)
        for tweet in (json_data['tweets']):
            if tweet != '':
                datafile_line = [y_label, tweet]
                data_file.append(datafile_line)

    return data_file
