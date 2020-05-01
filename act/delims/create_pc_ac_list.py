#!/usr/bin/env python
# coding: utf-8

# In[2]:


import os
from pathlib import Path
import PyPDF2
import sys
import re

def break_line(line):
    rows = list()
    items = re.split(r'(\d+)', line.strip())
    pc_no = items[1]
    pc_name = items[2][1:].strip()
    if('(' in pc_name):
        pc_classification = pc_name[pc_name.find('(')+1:pc_name.find(')')]
        pc_name = pc_name[0:pc_name.find('(')-1]
    else:
        pc_classification = 'General'
    
    for index in range(3, len(items)-1, 2):
        ac_no = items[index]
        index += 1
        ac_name = items[index][1:].replace('&', '').replace(' and ', '').replace(',', '').replace('.', '').strip()
        if('(' in ac_name):
            ac_classification = ac_name[ac_name.find('(')+1:ac_name.find(')')]
            ac_name = ac_name[0:ac_name.find('(')-1]
        else:
            ac_classification = 'General'
        
        row = pc_no + ',' + pc_name + ',' + pc_classification + ','                 + ac_no + ',' + ac_name + ',' + ac_classification
        rows.append(row)
        
    return rows

if __name__ == '__main__':
    
    #Give me delimited file from ECI in the format as Bihar_Delimitation.pdf
    #Spits out mapping of AC to PC and PC and AC Names in English
    
    cwd = os.getcwd()
    #name = sys.argv[1]
    name = 'Bihar'
    filepath = str(Path(cwd).parent.parent)+'/docs/delims/'+name+'_delimitation.pdf'
    
    pdf = PyPDF2.PdfFileReader(open(filepath, 'rb'))
    pages = pdf.numPages
    
    all_words = list()
    
    for i in range(0, pages):
        page = pdf.getPage(i)
        words = page.extractText().split(' ')
        all_words.extend(words)
    
    line = ''
    lines = list()
    
    for word in all_words:
        if(re.match(r'^\d+\.$', word)):
            lines.append(line)
            line = word.strip()
        elif(word.isdigit()): #is only page number, skip
            continue
        elif('NOTE' in word): #signifies end of usable data
            lines.append(line)
            break
        else:
            line += word.strip() + ' '
    
    all_rows = list() 
    
    for line in lines:
        if(re.match(r'^\d+\.', line)):
            line = re.sub(' +', ' ', line).replace('\t', '').replace('\r', '').replace('\n', '')
            #print('Line:' + line)
            rows = break_line(line)
            all_rows.extend(rows)
        else:       #useless line, skip
            continue
    
    print('pc_no, pc_name, pc_classification, ac_no, ac_name, ac_classification')
    for row in all_rows:
        print (row)


# In[ ]:




