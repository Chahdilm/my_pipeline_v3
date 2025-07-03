
from bin.path_variable import *

import os 
import time
import sys

import json 


from pyhpo import Ontology,HPOSet
Ontology(PATH_INPUT_HPO,transitive=True)
print(Ontology.version())



import pandas as pd
import numpy as np

import yaml

import logging

import glob

import argparse
 
import networkx as nx
import matplotlib.pyplot as plt
 
import seaborn as sns

import logging

from difflib import SequenceMatcher # for compare rank factors 2

import argparse


"""

#import collections # for count nb of hpo in patient or orphacode
import pandas as pd 
import numpy as np 
import os 
import math
import json
import collections
import sys
import time
import glob

#import asyncio

#import pytest # importing our library of test

import warnings
warnings.simplefilter(action='ignore', category=UserWarning)

import concurrent.futures

import logging

from pyhpo import Ontology,HPOSet # hpo3

import itertools # to get all association

# for plot only
import matplotlib.pyplot as plt
import seaborn as sns




import networkx as nx

#starting times
start_time = time.perf_counter() # in the file libray
Ontology()
print("End Load pyhpo\ttime : \t%s seconds" % (time.perf_counter() - start_time)) # 27 sec



"""