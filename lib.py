from __future__ import division
from sql_lib import sql, get_sql_db_table
from links import all
from wget import download
from time import time
from statistics import pstdev
import os, shutil, math

def get_file_path():

    cwd = os.getcwd() + '/data/'
    csv_1 = []  #for big data (sp,ge,fr, etc. )
    csv_2 = []  #for small data (ro, pol, arg, etc.)

    for root, dirs, files in os.walk(cwd):
        for f in files:

            if f.endswith('csv') and '_' in f:
                csv_1.append(root + '/' + f)

            elif f.endswith('csv') and '_' not in f and 'analiza' not in f:
                csv_2.append(root + '/' + f)

    data = {'big': csv_1, 'small': csv_2}
    return data

def get_csv():
    
    #get current working directory
    path = os.getcwd()+'/data/'

    start = time()

    #create list of countries
    countries = []

    for key,value in all.items():
        country = key.split('_')[0]
        #if country not in countries:
        #    countries.append(country)

        #creating folder for country if it does not exist
        if not os.path.exists(path+country):
            os.makedirs(path+country)

        if isinstance(value, dict):
            for k,v in value.items():
                if k >= 2018:
                    output1 = path+country+'/'+key+'_'+str(k)+'.csv'
                    file1 = download(v, out = output1)
                    if os.path.exists(output1):
                        shutil.move(file1, output1)

        elif isinstance(value, str):
            output2 = path+country+'/'+country+'.csv'
            file2 = download(value, out = output2)
            if os.path.exists(output2):
                shutil.move(file2, output2)

    print '\nIt took %.1f seconds to download all files' %(time()-start)

def recreate_small(filename):
    
    content = open(filename, 'r').readlines()
    content.pop(0)
    header = 'Div,Date,HomeTeam,AwayTeam,FTHG,FTAG\r\n'

    """
    f2012 = open(filename.replace('.csv', '_1_2012.csv'), 'w')
    f2012.write(header)
    f2013 = open(filename.replace('.csv', '_1_2013.csv'), 'w')
    f2013.write(header)
    f2014 = open(filename.replace('.csv', '_1_2014.csv'), 'w')
    f2014.write(header)
    f2015 = open(filename.replace('.csv', '_1_2015.csv'), 'w')
    f2015.write(header)
    """
    f2016 = open(filename.replace('.csv', '_1_2016.csv'), 'w')
    f2016.write(header)
    f2017 = open(filename.replace('.csv', '_1_2017.csv'), 'w')
    f2017.write(header)
    f2018 = open(filename.replace('.csv', '_1_2018.csv'), 'w')
    f2018.write(header)
   
    for line in content:
        line = [l.strip() for l in line.split(',')]

        if line[2][:4] == '2018':
            f2018.write('%s,%s,%s,%s,%s,%s\r\n' %(line[1], line[3], line[5], line[6], line[7], line[8]))
        elif line[2][:4] == '2017':
            f2017.write('%s,%s,%s,%s,%s,%s\r\n' %(line[1], line[3], line[5], line[6], line[7], line[8]))
        elif line[2][:4] == '2016':
            f2016.write('%s,%s,%s,%s,%s,%s\r\n' %(line[1], line[3], line[5], line[6], line[7], line[8]))
        """
        elif line[2][:4] == '2015':
            f2015.write('%s,%s,%s,%s,%s,%s\r\n' %(line[1], line[3], line[5], line[6], line[7], line[8]))
        elif line[2][:4] == '2014':
            f2014.write('%s,%s,%s,%s,%s,%s\r\n' %(line[1], line[3], line[5], line[6], line[7], line[8]))
        elif line[2][:4] == '2013':
            f2013.write('%s,%s,%s,%s,%s,%s\r\n' %(line[1], line[3], line[5], line[6], line[7], line[8]))
        elif line[2][:4] == '2012':
            f2012.write('%s,%s,%s,%s,%s,%s\r\n' %(line[1], line[3], line[5], line[6], line[7], line[8]))
    
    f2012.close()
    f2013.close()
    f2014.close()
    f2015.close()
    """
    f2016.close()
    f2017.close()
    f2018.close()

    return True

def analiza(filename):

    content = file(filename, 'r').readlines()
    content.pop(0)
    
    ga = gd = m = 0
    ga0 = ga1 = ga2 = ga3 = ga4 = 0
    gd0 = gd1 = gd2 = gd3 = gd4 = 0
    for line in content:
        
        line = [l.strip() for l in line.split(',')]
        
        if line[4] == '':
            line[4] = 0
            line[5] = 0

        ga += int(line[4])
        gd += int(line[5])
        m += 1
        
        if int(line[4]) == 0:
            ga0 += 1
        elif int(line[4]) == 1:
            ga1 += 1
        elif int(line[4]) == 2:
            ga2 += 1
        elif int(line[4]) == 3:
            ga3 += 1
        elif int(line[4]) == 4:
            ga4 += 1
        if int(line[5]) == 0:
            gd0 += 1
        elif int(line[5]) == 1:
            gd1 += 1
        elif int(line[5]) == 2:
            gd2 += 1
        elif int(line[5]) == 3:
            gd3 += 1
        elif int(line[5]) == 4:
            gd4 += 1

    mga = ga/m   
    mgd = gd/m

    return_dict = {}
    return_dict['nume'] = filename.split('/')[-1].rstrip('.csv')
    #return_dict['mga'] = float(format(mga, '.4f'))
    #return_dict['mgd'] = float(format(mgd, '.4f'))
    return_dict['m'] = m

    return_dict['sga'] = []
    return_dict['sgd'] = []

    for i in range(5):
        for j in ['ga', 'gd']:
            return_dict['%s%s' %(j,i)] = float(format(locals()['%s%s' %(j,i)]/m*100, '.2f'))
            return_dict['p%s%s' %(i,j)] = float(format(poisson(i, locals()['m%s' %j])*100, '.2f'))
    
    for i in range(5):
        return_dict['sga'].append(float(format(return_dict['ga%s' %i] - return_dict['p%sga' %i], '.2f')))
        return_dict['sgd'].append(float(format(return_dict['gd%s' %i] - return_dict['p%sgd' %i], '.2f')))
    
    return_dict['sdga'] = pstdev(return_dict['sga'])
    return_dict['sdgd'] = pstdev(return_dict['sgd'])

    return return_dict

def analiza_csv():
    f = open('data/analiza.csv', 'w')
    
    for filename in get_file_path()['big']:
        a = analiza(filename)

        f.write("%s,Meciuri:,%s,,,,,\r\n" %(a['nume'], a['m']))
        f.write("G,PA,A,dA,PD,D,dD\r\n")
        for i in range(5):
            f.write("%s,%s,%s,%s,%s,%s,%s\r\n" %(i, a['p%sga' %i], a['ga%s' %i], 
                                                    a['ga%s' %i] - a['p%sga' %i],
                                                    a['p%sgd' %i], a['gd%s' %i], 
                                                    a['gd%s' %i] - a['p%sgd' %i]))

        f.write(",,,,,,\r\n")
    f.close()

def analiza_sql(db = None):

    db = 'data/analiza.db' if db is None else db
    
    for filename in get_file_path()['big']:
        
        tb = filename[-8:-4]
        data = analiza(filename)
        
        sql_data = {}
        sql_data['name'] = data['nume'][:-5]
        sql_data['sdga'] = float(format(data['sdga'], '.3f'))
        sql_data['sdgd'] = float(format(data['sdgd'], '.3f'))
        
        sql().add_value(db = db, tb = tb, **sql_data)

def get_league(echipa, an):

    ani = 'data/all_%s.db' %an
    if not os.path.isfile(ani):
        print '%s nu exista' %ani
        return False

    tari = get_sql_db_table(db = ani)
    for tara in tari:
        echipe = sql().get_data(db = ani, tb = tara, field = 'name')
        for ech in echipe[1:]:
            if echipa == ech[0]:
                return tara

def poisson(x, mean):

    exp = math.exp(1)
    
    return float(format(exp**(-mean)*mean**x/math.factorial(x), '.5f'))

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
    print '%s %s - %s vs %s' %(liga_e1, an, e1, e2)
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
