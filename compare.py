from __future__ import division
from lib import poisson
from sql_lib import sql
from re import match

def match_to_match(filename):
    
    content = file(filename, 'r').readlines()
    data = {}
    content.pop(0)
    e = 2.71828

    tara = '_'.join(filename.split('/')[-1].split('_')[:2])
    an =  filename.split('/')[-1].split('_')[-1].rstrip('.csv')
    
    replace_dict = {'CS U. Craiova': 'U Craiova 1948 CS',
                    'Daco-Getica Bucuresti': 'FC Juventus Bucuresti',
                    'FC Viitorul': 'Viitorul Constanta'}
    values = ['gda', 'gpa', 'gdd', 'gpd', 'va', 'ea', 'ia', 'vd', 'ed', 'id']
    ignore_teams = ['Neustadt', 'Chindia Targoviste', 'UTA Arad']
 
    fl = open('results/res_%s' %(filename.split('/')[-1]), 'w')
    fl.write('meci,procent,scor,,,victorie,,,amb. marc,,,peste 2_5,,\r\n')
    
    tara_res = {}
    tara_res['name'] = tara
    tara_res['scor'] = 0
    tara_res['v'] = 0
    tara_res['am'] = 0
    tara_res['p2_5'] = 0
    tara_res['tot'] = 0

    for line in content:
        line = [l.strip() for l in line.split(',')]
        
        for rk, rv in replace_dict.items():
            line = [j.replace(rk, rv) for j in line]

        if line[2] in ignore_teams or line[3] in ignore_teams:
            break

        if line[2] not in data.keys():
            data[line[2]] = {}
            data[line[2]]['mdate'] = []
            data[line[2]]['mjt'] = 0

        if line[3] not in data.keys():
            data[line[3]] = {}
            data[line[3]]['mdate'] = []
            data[line[3]]['mjt'] = 0

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
            data[line[2]]['mjt'] += 1
            data[line[3]]['mjt'] += 1
            data[line[2]]['mdate' ].append(''.join(line[1].split('/')[::-1]) + '+2')
            data[line[3]]['mdate' ].append(''.join(line[1].split('/')[::-1]) + '-2')

        elif line[4] < line[5]:
            data[line[2]]['ia'] += 1
            data[line[3]]['vd'] += 1
            data[line[2]]['mjt'] += 1
            data[line[3]]['mjt'] += 1
            data[line[2]]['mdate' ].append(''.join(line[1].split('/')[::-1]) + '-3')
            data[line[3]]['mdate' ].append(''.join(line[1].split('/')[::-1]) + '+3')

        else:
            data[line[2]]['ea'] += 1
            data[line[3]]['ed'] += 1
            data[line[2]]['mjt'] += 1
            data[line[3]]['mjt'] += 1           
            data[line[2]]['mdate' ].append(''.join(line[1].split('/')[::-1]) + '+0')
            data[line[3]]['mdate' ].append(''.join(line[1].split('/')[::-1]) + '+1')
        
        data[line[2]]['scor'] = 0
        data[line[2]]['v'] = 0
        data[line[2]]['am'] = 0
        data[line[2]]['p2_5'] = 0
        data[line[2]]['tot'] = 0

        data[line[3]]['scor'] = 0
        data[line[3]]['v'] = 0
        data[line[3]]['am'] = 0
        data[line[3]]['p2_5'] = 0
        data[line[3]]['tot'] = 0

        if data[line[2]]['mjt'] >= 10 and data[line[3]]['mjt'] >= 10:
            for key,val in data.items():
                val['mja'] = val['va'] + val['ea'] + val['ia']
                val['mgda'] = float(format(val['gda']/val['mja'], '.2f'))
                val['mgpa'] = float(format(val['gpa']/val['mja'], '.2f'))
                val['mjd'] = val['vd'] + val['ed'] + val['id']
                val['mgdd'] = float(format(val['gdd']/val['mjd'], '.2f'))
                val['mgpd'] = float(format(val['gpd']/val['mjd'], '.2f'))

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
                    #fa = data[line[2]]['forta']
                    #fd = data[line[3]]['forta']
                    fa = 1
                    fd = 1
                    probs['%s-%s' %(i,j)] = float(format((fa*data[line[2]]['p%sgda' %i] * \
                                                          fd*data[line[3]]['p%sgdd' %j])/100, '.2f'))
                    sums += probs['%s-%s' %(i,j)]
            
            if sums >= 95:
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
                
                if scor == pscor:
                    tara_res['scor'] += 1
                    tara_res['tot'] += 1
                else:
                    tara_res['tot'] += 1

                if v == pv:
                    tara_res['v'] += 1

                if am == pam:
                    tara_res['am'] += 1

                if p2_5 == pp2_5:
                    tara_res['p2_5'] += 1


                fl.write('%s-%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\r\n'
                        %(line[2], line[3], sums, scor, pscor, 
                          1 if scor == pscor else 0, 
                          v, pv, 1 if v==pv else 0, am, pam, 
                          1 if am==pam else 0, p2_5, pp2_5,
                          1 if p2_5==pp2_5 else 0))

    if int(an) < 2018:
        tara_res['scor'] = float(format(tara_res['scor']/tara_res['tot']*100, '.1f'))
        tara_res['v'] = float(format(tara_res['v']/tara_res['tot']*100, '.1f'))
        tara_res['am'] = float(format(tara_res['am']/tara_res['tot']*100, '.1f'))
        tara_res['p2_5'] = float(format(tara_res['p2_5']/tara_res['tot']*100, '.1f'))
    
        sql().add_value(db = 'results/all_res_o95.db' , tb = 'all_%s' %an, **tara_res)

    #print tara_res
