from __future__ import division
from sql_lib import sql
from get_csv import get_file_path
from re import match
import os, math

def data_p(filename):
    
    content = file(filename, 'r').readlines()
    data = {}
    content.pop(0)
    e = 2.71828

    replace_dict = {'CS U. Craiova': 'U Craiova 1948 CS',
                    'Daco-Getica Bucuresti': 'FC Juventus Bucuresti',
                    'FC Viitorul': 'Viitorul Constanta'}
    values = ['gda', 'gpa', 'gdd', 'gpd', 'va', 'ea', 'ia', 'vd', 'ed', 'id']
    ignore_teams = ['Neustadt', 'Chindia Targoviste', 'UTA Arad']

    for line in content:
        line = [l.strip() for l in line.split(',')]
        
        for rk, rv in replace_dict.items():
            line = [j.replace(rk, rv) for j in line]

        if line[2] in ignore_teams or line[3] in ignore_teams:
            break

        if line[2] not in data.keys():
            data[line[2]] = {}
            data[line[2]]['mdate'] = []

        if line[3] not in data.keys():
            data[line[3]] = {}
            data[line[3]]['mdate'] = []

        for val in values:
            for index in [2,3]:
                if val not in data[line[index]].keys():
                    data[line[index]][val] = 0

        if line[4] == '':
            line[4] = 0
        if line[5] == '':
            line[5] = 0

        data[line[2]]['gda'] += int(line[4])
        data[line[2]]['gpa'] += int(line[5])
        data[line[3]]['gdd'] += int(line[5])
        data[line[3]]['gpd'] += int(line[4])

        if line[4] > line[5]:
            data[line[2]]['va'] += 1
            data[line[3]]['id'] += 1
            data[line[2]]['mdate' ].append(''.join(line[1].split('/')[::-1]) + '+2')
            data[line[3]]['mdate' ].append(''.join(line[1].split('/')[::-1]) + '-2')

        elif line[4] < line[5]:
            data[line[2]]['ia'] += 1
            data[line[3]]['vd'] += 1
            data[line[2]]['mdate' ].append(''.join(line[1].split('/')[::-1]) + '-3')
            data[line[3]]['mdate' ].append(''.join(line[1].split('/')[::-1]) + '+3')

        else:
            data[line[2]]['ea'] += 1
            data[line[3]]['ed'] += 1
            data[line[2]]['mdate' ].append(''.join(line[1].split('/')[::-1]) + '+0')
            data[line[3]]['mdate' ].append(''.join(line[1].split('/')[::-1]) + '+1')

    for key,val in data.items():

        val['mja'] = val['va'] + val['ea'] + val['ia']
        val['mgda'] = float(format(val['gda']/val['mja'], '.2f'))
        val['mgpa'] = float(format(val['gpa']/val['mja'], '.2f'))
        val['mjd'] = val['vd'] + val['ed'] + val['id']
        val['mgdd'] = float(format(val['gdd']/val['mjd'], '.2f'))
        val['mgpd'] = float(format(val['gpd']/val['mjd'], '.2f'))
        val['mjt'] = val['mja']+val['mjd']

        val['pct'] = (val['va'] + val['vd'])*3 + (val['ea'] + val['ed'])*1
        val['fa'] = float(format((val['va']-val['ia'])*100/val['mja'], '.1f'))
        val['fd'] = float(format((val['vd']-val['id'])*100/val['mjd'], '.1f'))
        val['mdate'] = sorted(val['mdate'], reverse = True)[:10]
        val['istoric'] = ''.join([i[-2:] for i in val['mdate']])
        val['forta'] = 100
        
        for i in range(0, 8, 2):
            val['forta'] += int(val['istoric'][i:i+2])

        for g in range(5):
            for t in ['gda', 'gpa', 'gdd', 'gpd']:
                val['p%s%s' %(g,t)] = float(format(e**(-val['m%s' %t])*val['m%s' %t]**g*100/math.factorial(g), '.2f'))

    export_list = ['mjt', 'pct', 'forta', 'fa', 'fd', 'p[0-4]g[d,p][a,d]']
    export_data = {}

    for key,val in data.items():
        export_data[key] = {}
        for k in val:
            for ex in export_list:
                if match(ex, k):
                    export_data[key][k] = data[key][k]

    return export_data

#inter = data_small('data/romania/romania.csv', year = 2017)['Astra']
#inter['name'] = 'Astra'
#sql().add_value(db = 'ro.db', tb = 'romania', **inter)
#for i,j in inter.items():
#    print "%s: %r" %(i,j)

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
