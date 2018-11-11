#!/usr/bin/env python

from create_sql import data_p
from lib import *
from sql_lib import sql

#get_csv()

for fl in get_file_path()['small']:
    recreate_small(fl)

analiza_csv()
    
analiza_sql()

for fl in get_file_path()['big']:
    year = fl.split('_')[-1].rstrip('.csv')
    liga = '_'.join(fl.split('/')[-1].split('_')[:2])
    print 'Starting %s %s' %(liga, year)
    dt = data_p(fl)
    if int(year) <= 2018:
        for k,v in sorted(dt.items()):
            dic = {'name': k}
            dic.update(v)
            sql().add_value(db = 'data/all_%s.db' %year, tb = liga, **dic)
