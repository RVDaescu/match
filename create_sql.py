from __future__ import division
from sql_lib import sql
from collections import OrderedDict
import os

def get_files():

    cwd = os.getcwd() + '/data/'
    csv_1 = []  #for big data (sp,ge,fr, etc. )
    csv_2 = []  #for small data (ro, pol, arg, etc.)

    for root, dirs, files in os.walk(cwd):
        for f in files:

            if f.endswith('csv') and '_' in f:
                csv_1.append(root + '/' + f)

            elif f.endswith('csv') and ')' not in f:
                csv_2.append(root + '/' + f)

    data = {'big': csv_1, 'small': csv_2}
    return data

def data_big(filename):
    content = file(filename, 'r').readlines()
    data = {}
    header = content.pop(0).split(',')

    for line in content:
        line = line.split(',')
        if line[2] not in data.keys():
            data[line[2]] = {}
        if 'gda' not in data[line[2]].keys():
            data[line[2]]['gda'] = 0
        if 'gpa' not in data[line[2]].keys():
            data[line[2]]['gpa'] = 0
        if 'gdd' not in data[line[2]].keys():
            data[line[2]]['gdd'] = 0
        if 'gpd' not in data[line[2]].keys():
            data[line[2]]['gpd'] = 0
        if 'va' not in data[line[2]].keys():
            data[line[2]]['va'] = 0
        if 'ea' not in data[line[2]].keys():
            data[line[2]]['ea'] = 0
        if 'ia' not in data[line[2]].keys():
            data[line[2]]['ia'] = 0
        if 'vd' not in data[line[2]].keys():
            data[line[2]]['vd'] = 0
        if 'ed' not in data[line[2]].keys():
            data[line[2]]['ed'] = 0
        if 'id' not in data[line[2]].keys():
            data[line[2]]['id'] = 0

    for line in content:
        line = line.split(',')

        data[line[2]]['gda'] += int(line[4])
        data[line[2]]['gpa'] += int(line[5])
        data[line[3]]['gdd'] += int(line[5])
        data[line[3]]['gpd'] += int(line[4])

        if line[4] > line[5]:
            data[line[2]]['va'] += 1
            data[line[3]]['id'] += 1

        elif line[4] < line[5]:
            data[line[2]]['ia'] += 1
            data[line[3]]['vd'] += 1

        elif line[4] == line[5]:
            data[line[2]]['ea'] += 1
            data[line[3]]['ed'] += 1
    
    for key,val in data.items():
        val['mja'] = val['va'] + val['ea'] + val['ia']
        val['mgda'] = float(val['gda']/val['mja'])
        val['mgpa'] = float(val['gpa']/val['mja'])
        val['mjd'] = val['vd'] + val['ed'] + val['id']
        val['mgdd'] = float(val['gdd']/val['mjd'])
        val['mgpd'] = float(val['gpd']/val['mjd'])
        
        #print key, val

    return data

inter = data_big('data/italia/italia_1_2018.csv')['Milan']
#for i,j in inter.items():
#    print "%s: %r" %(i,j)


for fl in get_files()['big']:
    year = fl
    liga = '_'.join(fl.split('/')[-1].split('.')[:-1])
    dt = data_big(fl)
    for k,v in sorted(dt.items()):
        dic = {'name': k}
        dic.update(v)
        sql().add_value(db = 'data/all_%s.db' %liga.split('_')[-1], tb = liga, **dic)
