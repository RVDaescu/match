#!/usr/bin/env python

from lib import *
from create_sql import *
from links import *
from sql_lib import *
import os

def prognoza(e1 = None, e2 = None, an = 2016):
    
    liga_e1 = get_league(e1, an = an)
    liga_e2 = get_league(e2, an = an)

    if not liga_e1:
        print 'Echipa %s nu exista' %e1
    if not liga_e2:
        print 'Echipa %s nu exista' %e2

    raw_e1 = sql().get_row(db = 'data/all_%s.db' %an, tb = liga_e1, lookup = e1)
    raw_e2 = sql().get_row(db = 'data/all_%s.db' %an, tb = liga_e2, lookup = e2)
    sums = 0
    probs = {}
    for i in range(5):
        for j in range(5):
            probs['%s-%s' %(i,j)] = float(format((raw_e1['p%sgda' %i] * raw_e2['p%sgdd' %j])/100, '.2f'))
            sums += probs['%s-%s' %(i,j)]
    
    print 'Suma procentelor este: %.2f %%\b' %sums 
    
    string = '\t0\t1\t2\t3\t4\n'
    for i in range(5):
        for j in range(5):
            if j == 0:
                string += '%s\t' %i + str(probs['%s-%s' %(i,j)])+'\t'
            elif j > 0 and j < 4:
                string += str(probs['%s-%s' %(i,j)])+'\t'
            elif j == 4:
                string += str(probs['%s-%s' %(i,j)])+'\n'
    print string

prognoza(e1 = 'Din. Bucuresti', e2 = 'FC Steaua Bucuresti')
