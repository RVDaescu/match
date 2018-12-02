#!/usr/bin/env python

from lib import *
from create_sql import *
from links import *
from sql_lib import *
from compare import *
import os

"""
for fl in get_file_path()['big']:
    year = fl.split('_')[-1].rstrip('.csv')
    liga = '_'.join(fl.split('/')[-1].split('_')[:2])
    print 'Starting %s %s' %(liga, year)
    dt = match_to_match(fl)
"""

match_to_match('data/argentina/argentina_1_2016.csv')
#data_p('data/austria/austria_1_2014.csv')
