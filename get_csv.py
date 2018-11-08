#!/usr/bin/env python

from links import all
from wget import download
from time import time
import os
import shutil

#based on links, will download csv's

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

get_csv()

