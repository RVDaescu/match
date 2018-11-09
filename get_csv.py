from __future__ import division
from links import all
from wget import download
from time import time
import os, shutil

def get_file_path():

    cwd = os.getcwd() + '/data/'
    csv_1 = []  #for big data (sp,ge,fr, etc. )
    csv_2 = []  #for small data (ro, pol, arg, etc.)

    for root, dirs, files in os.walk(cwd):
        for f in files:

            if f.endswith('csv') and '_' in f:
                csv_1.append(root + '/' + f)

            elif f.endswith('csv') and '_' not in f:
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
                if k == 2018:
                    output1 = path+country+'/'+key+'_'+str(k)+'.csv'
                    file1 = download(v, out = output1)
                    if os.path.exists(output1):
                        shutil.move(file1, output1)

        elif isinstance(value, str):
            output2 = path+country+'/'+country+'.csv'
            file2 = download(value, out = output2)
            if os.path.exists(output2):
                shutil.move(file2, output2)

    print '\nIt took %.2f seconds to download all files' %(time()-start)

def move_small(filename):

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

def d_check(filename):

    content = file(filename, 'r').readlines()
    content.pop(0)
    
    ga = gd = m = 0
    ga0 = ga1 = ga2 = ga3 = ga4 = 0
    gd0 = gd1 = gd2 = gd3 = gd4 = 0
    for line in content:
        
        line = [l.strip() for l in line.split(',')]
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
    return_dict['mga'] = float(format(mga, '.4f'))
    return_dict['mgd'] = float(format(mgd, '.4f'))
    for i in range(5):
        for j in ['ga', 'gd']:
            return_dict['%s%s' %(j,i)] = locals()['%s%s' %(j,i)]
    
    return return_dict
