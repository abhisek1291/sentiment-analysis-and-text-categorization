#################################
# Author : Abhisek Mohanty
# Description : Contains methods to generate and read files to and from teh disk.
#################################

import json
import os

current_directory = os.path.dirname(os.path.realpath(__file__))


def generateFile(data, subdirectory, filename, mode):
    '''
    creates a file on disk with the data and other parameters
    '''
    try:
        os.mkdir(subdirectory)
    except Exception:
        pass

    with open(os.path.join(subdirectory, '%s.json' % filename), mode) as f:
        f.write(json.dumps(data, indent=4))


def readFileFromDisk(subdirectory, filename): # Should add file type ???
    '''
    Read data from Disk.
    '''
    # print current_directory
    # print os.path.join(current_directory, subdirectory, '%s.json' % filename)
    # print subdirectory + '\t' + filename
    with open(os.path.join(subdirectory, '%s.json' % filename), 'r') as text_file:
        data = json.load(text_file)
    return data
