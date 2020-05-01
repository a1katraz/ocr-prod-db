#!/usr/bin/python
# -*- coding: utf-8 -*-
import io
import os
from google.cloud import storage
import csv
import os
import sys
from pathlib import Path
from translate import Translator

if __name__ == '__main__':
    
    #using MSFT service because it's more free
    
    cwd = os.getcwd()
    from_lang = 'hi'
    to_lang = 'en'
    secret = '1212d7d306fb4388a534e586691d0b57'
    trans = Translator(provider='microsoft', from_lang=from_lang, to_lang=to_lang, secret_access_key=secret)
    ac_no = sys.argv[1]
    #ac_no = str(238)
    
    with open(str(cwd)+'/dict/'+ac_no+'_booth_list.csv') as file:
        csv_reader = csv.reader(file, delimiter=',')
        line = 0
        for row in csv_reader:
            if (line == 0):
                print(','.join(row))
            else:
                ac_name = trans.translate(row[1]).strip()
                booth_name = trans.translate(row[3].replace('_', ',')).replace(',', '_').strip()
                print(row[0]+','+ac_name+','+row[2]+','+booth_name)
            line += 1
            