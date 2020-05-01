#!/usr/bin/env python
# coding: utf-8

# In[72]:


import os
import requests
import uuid
import json
import csv
import sys
from pathlib import Path

def make_connection(language, fromScript, toScript):
    subscription_key = '1212d7d306fb4388a534e586691d0b57'
    endpoint = 'https://api.cognitive.microsofttranslator.com'
    path = '/transliterate?api-version=3.0'
    params = '&language='+language+'&fromScript='+fromScript+'&toScript='+toScript
    constructed_url = endpoint + path + params
    
    headers = {
    'Ocp-Apim-Subscription-Key': subscription_key,
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
    }
    
    return constructed_url, headers
    

def transliterate(url, headers, array):
    body_json = []
    for items in array:
        dict = {'Text':items}
        body_json.append(dict)

    request = requests.post(url, headers=headers, json=body_json)
    response = request.json()
    
    result = list() 
    for item in response:
        result.append(item['text'].title())
    
    return result

if __name__ == '__main__':
   
    url, headers = make_connection(language='hi', fromScript='deva', toScript='latn')
    
    ac_no = sys.argv[1]
    cwd = os.getcwd()
    
    all_words = list()
    dict = {}    
    
    with open(str(cwd)+'/dict/'+ac_no+'_booth_list.csv') as file:
        csv_reader = csv.reader(file, delimiter=',')
        line = 0
        for row in csv_reader:
            if (line == 0):
                print(','.join(row))
            else:
                ac_names = (row[1]+' '+row[3].replace('_', ' ')).replace(u'\u200d', '').replace(u'\u200c', '').split(' ')
                for item in ac_names:
                    if(len(item) > 2 and item not in all_words):
                        all_words.append(item)    
            line += 1

    grps_10 = [all_words[n:n+10] for n in range(0, len(all_words), 10)]
    
    for words in grps_10:
        res = transliterate(url, headers, words)
        for i in range(0, len(res)):
            dict[words[i]] = res[i]
    
    with open(str(cwd)+'/dict/'+ac_no+'_booth_list.csv') as file:
        csv_reader = csv.reader(file, delimiter=',')
        line = 0
        for row in csv_reader:
            if (line > 0):
                ac_eng_name = ''
                ac_parts = row[1].replace('_', ' ').replace(u'\u200d', '').replace(u'\u200c', '').split(' ')
                for part in ac_parts:
                    if(len(part) > 2):
                        ac_eng_name = ac_eng_name + ' ' + dict[part]
                ac_eng_name.strip()

                booth_eng_name = ''
                booth_parts = row[3].replace('_', ' ').replace(u'\u200d', '').replace(u'\u200c', '').split(' ')
                for part in booth_parts:
                    if(len(part) > 2):
                        booth_eng_name = booth_eng_name + ' ' + dict[part]
                booth_eng_name.strip()
                
                print(row[0] + ',' + ac_eng_name + ',' + row[2] + ',' + booth_eng_name)

            line += 1
    


# In[ ]:




