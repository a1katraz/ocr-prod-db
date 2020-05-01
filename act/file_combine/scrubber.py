#!/usr/bin/env python
# coding: utf-8

# In[17]:


import os
from google.cloud import storage
import pandas
import re
import logging

def get_names_order(filename):
    return int(filename.split('.')[0].split('_')[3])

def choose3(gender):
    gender = gender.replace('"','').replace('"', '').replace('|', '').strip()
    if(gender.startswith('पु')):
        return 'M'
    elif(gender.startswith('म')):
        return 'F'
    elif(gender.startswith('तृ')):
        return 'T'
    else:
        return 'U'

def cleanup(a):
    if(isinstance(a, str)):
        return ''.join(re.findall(r'\d+\.', a))
    else:
        return a
    
    
if __name__ == '__main__':
    storage_client = storage.Client.from_service_account_json('/home/vishalvivek8/key.json')
    bucket = storage_client.bucket('raw_images_ocr')
    blobs = bucket.list_blobs(prefix = 'outputs/')
    cwd = os.getcwd()
    
    output_files = list()
    
    for blob in blobs:
        if(blob.name == 'outputs/' or blob.name.startswith('outputs/AC')):
            continue
        output_files.append(blob.name.replace('outputs/', ''))
    
    output_files.sort(key = get_names_order)
    
    final_file = open('AC_CombinedFile.csv', 'w')
    
    counter = 1
    
    for file in output_files:
        try:
            blob = bucket.blob('outputs/'+file)
            blob.download_to_filename(file)
            print ("Reading File:" + file)
            df = pandas.read_csv(file, header = 0, sep = ',', encoding = 'utf8', error_bad_lines = False)
            
            df.rename(columns={'Election Year':'El_Year', ' Assembly constituency':'State',                               ' AC No.':'AC_No', ' PC No.':'PC_No', ' Part No.':'Booth_No',                                ' 			ERPD':'Creation_Date', ' Serial No.': 'Serial_No',                                ' 			Voter ID':'EPIC', ' Voter Name': 'Voter_Name',                                ' Fathers name':'Father_Name', ' Age': 'Age', ' Gender': 'Gender',                                ' House No.':'House_No', ' Address details':'Address', ' Voter Surname':'Surname'
                              }, inplace = True)
            
           
            #df.dropna(axis = 0, how ='any', inplace = True)
            
            df['El_Year'] = 2020
            df['State'] = 'Bihar'
            df['AC_No'] = re.search(r'\d+',file.split('.')[0].split('_')[2]).group(0)
            df['PC_No'] = 39
            df['Booth_No'] = file.split('.')[0].split('_')[3]
            df['Creation_Date'] = '2020-02-07'
            df['Serial_No'] = df['Serial_No'].map(lambda a: "".join(re.findall(r'\d+', str(a))), na_action='ignore')
            df['EPIC'] = df['EPIC'].map(lambda a:a.replace('"','').replace('"', '').replace('।', '1').strip(), na_action='ignore')
            df['Voter_Name'] = df['Voter_Name'].map(lambda a:a.replace('"','').replace('"', '').replace('।', '1').strip(), na_action='ignore')
            df['Father_Name'] = df['Father_Name'].map(lambda a:a.replace('"','').replace('"', '').replace('।', '1').strip(), na_action='ignore')
            #df['Age'] = df['Age'].map(cleanup, na_action='ignore') #only complicates matters
            df['Gender'] = df['Gender'].map(choose3, na_action='ignore')
            #df['House_No'] = df['House_No'].map(cleanup, na_action='ignore')
            df['Address'] = df['Address'].map(lambda a:a.replace('"','').replace('"', '').replace('।', '1').strip(), na_action='ignore')
            df['Surname'] = df['Surname'].map(lambda a:a.replace('"','').replace('"', '').replace('।', '1').strip(), na_action='ignore')
            
            df = df[['State', 'El_Year', 'PC_No', 'AC_No', 'Booth_No', 'Creation_Date', 'Serial_No', 'EPIC',                    'Voter_Name', 'Father_Name', 'Age', 'Gender', 'House_No', 'Address', 'Surname'
                    ]]
            
            #print(df['Age'])
            #df.dropna(axis = 0, how ='any', inplace = True) #no loose ends - condition very harsh, drops around 10% of electorate
                        
            df.to_csv(final_file, header = False, encoding = 'utf-8-sig', index = False)
            final_file.flush()
            
        except pandas.errors.ParserError as e:
            error_line = str(e)
            i = int(re.findall(r'\d+', error_line)[0])
            if(i <= len(df.index)):  
                df.drop(df.index[i])

            df.to_csv(final_file, header = False, encoding = 'utf-8-sig', index = False)
            final_file.flush()
            
        except Exception as e:
            print('Missed reading file '+file+' because of error:' + str(e))
            logging.exception("message")
            
        finally:
            os.remove(file)
        
    final_file.close()
    
    save_blob = bucket.blob('outputs/AC_CombinedFile.csv')
    save_blob.upload_from_filename('AC_CombinedFile.csv')


# In[ ]:




