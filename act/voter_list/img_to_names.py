#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import PIL
from os import listdir
from os.path import isfile, join
# from names import get_names
from names_cv import get_names_cv
from headers_cv import get_headers
import gc


def filenum(fname):
    return int(fname[3:len(fname) - 4])


def get_files(directory):

    dirpath = directory+'/images/voter_list'
    # print(dirpath)
    
    files = [f for f in listdir(dirpath) if isfile(join(dirpath, f))]

    # print(files)

    files.sort()
    files.sort(key=filenum)
    for x in range(0, len(files)):
        files[x] = dirpath + '/' + files[x]
    return files


def convert_to_names(out_name):
    cwd = os.path.abspath(os.getcwd())
    
    # ....print (cwd)
    
    f_names = get_files(cwd)
    f = open(cwd + '/'+out_name+'.csv', 'w+')
    f.write('Election Year,Assembly constituency,AC No.,AC Reservation,\
            Parliamentary constituency,PC No.,PC Reservation,Part No.,\
            ERPD,Booth Name,\
            Booth No.,PIN Code,Serial No.,\
            Voter ID, Voter Name,Fathers name,Age,Gender,House No.,Address details,\
            Voter Surname,Grouped Surname,Linked Caste,ERRORS\n'
            )

    serial = 1

    # len(f_names)-1-2
    # ###Translate first file

    header_details = get_headers(f_names[0])
    appendix_page = 0
    os.remove(f_names[0])
    
    for x in range(1, len(f_names) - 1):
        (name_list, counter, appendix_page) = get_names_cv(f_names[x],
                serial, appendix_page)
        for name_tuple in name_list:

        # ....print >> f, name_tuple

            name_tuple = header_details + name_tuple
            f.write(','.join(str(item) for item in name_tuple))
            f.write('\n')
        if x % 10 == 0:
            gc.collect()
     
        os.remove(f_names[x])
        f.flush()
        serial = serial + counter

    os.remove(f_names[len(f_names)-1])

    f.close()
    return cwd+'/'+out_name+'.csv'
