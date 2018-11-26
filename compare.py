from __future__ import division
from lib import poisson
from re import match

def match_to_match(filename):
    
    content = file(filename, 'r').readlines()
    data = {}
    content.pop(0)
    e = 2.71828

    replace_dict = {'CS U. Craiova': 'U Craiova 1948 CS',
                    'Daco-Getica Bucuresti': 'FC Juventus Bucuresti',
                    'FC Viitorul': 'Viitorul Constanta'}
    values = ['gda', 'gpa', 'gdd', 'gpd', 'va', 'ea', 'ia', 'vd', 'ed', 'id']
    ignore_teams = ['Neustadt', 'Chindia Targoviste', 'UTA Arad']
 
    fl = open('comp/res_%s' %(filename.split('/')[-1]), 'w')
    
    fl.write('meci,procent,scor,,victorie,,amb. marc,,peste 2_5,\r\n')
    
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
    
        if len(data[line[2]]['mdate']) >= 10 and len(data[line[3]]['mdate']) >= 10:
            for key,val in data.items():
                val['mja'] = val['va'] + val['ea'] + val['ia']
                try:
                    val['mgda'] = float(format(val['gda']/val['mja'], '.2f'))
                except:
                    print val['mja']
                    print filename, line[2], line[3], data[line[2]]['mja'], data[line[3]]['mja']

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
                val['forta'] = 1
                
                for i in range(0, 10, 2):
                    val['forta'] +=int(val['istoric'][i:i+2])/100
                
                for g in range(5):
                    for t in ['gda', 'gpa', 'gdd', 'gpd']:
                        val['p%s%s' %(g,t)] = float(format(poisson(g, val['m%s' %t])*100, '.3f'))
            
            scor = '%s-%s' %(line[4], line[5])
            
            if int(line[4]) + int(line[5]) > 2.5:
                p2_5 = 'da'
            else:
                p2_5 = 'nu'
            
            if line[4] > line[5]:
                v = 'va'
            elif line[4] < line[5]:
                v = 'vd'
            else:
                v = 'e'
            
            if int(line[4]) == 0 or int(line[5]) == 0:
                am = 'nu'
            else:
                am = 'da'
                    
            probs = {}
            sums = 0
            for i in range(5):
                for j in range(5):
                    probs['%s-%s' %(i,j)] = float(format((data[line[2]]['p%sgda' %i] * data[line[3]]['p%sgdd' %j])/100, '.2f'))
                    sums += probs['%s-%s' %(i,j)]
            
            pp2_5 = 0
            pva = 0
            pe = 0
            pvd = 0
            pam = 0
            pdm = 0

            for i in range(5):
                for j in range(5):
                    if i + j > 2.5:
                        pp2_5 += probs['%s-%s' %(i,j)]

                    if i > j:
                        pva += probs['%s-%s' %(i,j)]
                    elif i < j:
                        pvd += probs['%s-%s' %(i,j)]
                    else:
                        pe += probs['%s-%s' %(i,j)]
                    
                    if i == 0 and j == 0:
                        pam += probs['%s-%s' %(i,j)]
                        pdm += probs['%s-%s' %(i,j)]
                    elif i == 0 and j != 0:
                        pam += probs['%s-%s' %(i,j)]
                    elif i != 0 and j == 0:
                        pdm += probs['%s-%s' %(i,j)]
            
            string = '\t0\t1\t2\t3\t4\n'
            for i in range(5):
                for j in range(5):
                    if j == 0:
                        string += '%s\t' %i + str(probs['%s-%s' %(i,j)])+'\t'
                    elif j > 0 and j < 4:
                        string += str(probs['%s-%s' %(i,j)])+'\t'
                    elif j == 4:
                        string += str(probs['%s-%s' %(i,j)])+'\n'
            #print string

            if pp2_5*2 >= sums:
                pp2_5 = 'da'
            else:
                pp2_5 = 'nu'

            if pva >= pe and pva >= pvd:
                pv = 'va'
            elif pe > pva and pe > pvd:
                pv = 'e'
            elif pvd > pva and pvd > pe:
                pv = 'vd'
            
            if pam*2 < sums or pdm*2 < sums:
                pam = 'nu'
            else:
                pam = 'da'

            pscor = probs.keys()[probs.values().index(max(probs.values()))]
            
            fl.write('%s-%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\r\n'
                    %(line[2], line[3], sums, scor, pscor, 
                      v, pv, am, pam, p2_5, pp2_5))
