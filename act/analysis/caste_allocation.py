#!/usr/bin/python
# -*- coding: utf-8 -*-
from google.cloud import storage
import os
import pandas
import re

def get_names_order(filename):
    return int(filename.split('.')[0].split('_')[3])

def vlookup_caste_rel(caste_col, castes, part_name):
    try:
        castes['Religion'].fillna('N', inplace=True)
        caste = caste_col.merge(castes, on='Title', how='left')
        c_freq = caste['Caste'].value_counts()
        c_freq.rename('Caste_Counts', inplace=True)
        if (len(caste_col.index) > c_freq.sum() and 'Others' in c_freq.index):
            c_freq['Others'] = c_freq['Others'] + len(caste_col.index) - c_freq.sum()
        elif (len(caste_col.index) > c_freq.sum()):
            others = pandas.Series([0], index=['Others'])
            c_freq.append(others)
            c_freq['Others'] = len(caste_col.index) - c_freq.sum()
        
        c_freq = c_freq.to_frame()
        file_array = [part_name] * len(c_freq.index)
        c_freq.insert(0, 'PartNo', file_array)
        c_freq.insert(1, 'Caste_Name', list(c_freq.index))
        
        
        r_freq = caste['Religion'].value_counts(dropna = False)
        r_freq.rename('Rel_Counts', inplace=True)
        r_freq.rename(index={'N':'Non-Muslim', 'M': 'Muslim'}, inplace = True)
        r_freq = r_freq.to_frame()
        file_array = [part_name] * len(r_freq.index)
        r_freq.insert(0, 'PartNo', file_array)
        r_freq.insert(1, 'Religion_Name', list(r_freq.index))
        
    except Exception as e:
        print('Some error in analysis.' + str(e))
    
    return c_freq, r_freq

if __name__ == '__main__':

    storage_client = storage.Client.from_service_account_json('/home/vishalvivek8/key.json')

    bucket = storage_client.bucket('raw_images_ocr')

    blobs = bucket.list_blobs(prefix='outputs/')
    
    cwd = os.getcwd()
    output_files = list()
    
    for blob in blobs:
        if(blob.name == 'outputs/' or 'CombinedFile' in blob.name):
            continue
        output_files.append(blob.name.replace('outputs/', ''))
    
    output_files.sort(key = get_names_order)
    final_caste_file = open('ACNo238_Caste_Allocation.csv', 'w')
    final_rel_file = open('ACNo238_Rel_Allocation.csv', 'w')
    counter = 1
    
    master_file = open(cwd+'/dict/238_caste_linkage.csv', 'r+')
    castes = pandas.read_csv(master_file, header = 0, sep = ',', encoding = 'utf8', error_bad_lines = False)
    
    master_c_frame = pandas.DataFrame(columns = ['PartNo', 'Caste_Name', 'Caste_Counts'])
    master_r_frame = pandas.DataFrame(columns = ['PartNo', 'Religion_Name', 'Rel_Counts'])
    
    for file in output_files:
        try:
            blob = bucket.blob('outputs/'+file)
            blob.download_to_filename(file)
            print ("Reading File:" + file)
            dataframe = pandas.read_csv(file, header = 0, sep = ',', encoding = 'utf8', error_bad_lines = False) 
            ind_castes = pandas.concat([dataframe[' Voter Surname']], axis = 1, keys=['Title'])
            
            c_hist, r_hist = vlookup_caste_rel(ind_castes, castes, file.split('.')[0].split('_')[3])
            
            if counter > 1:
                c_hist.to_csv(final_caste_file, index=False, header = False)
                r_hist.to_csv(final_rel_file, index=False, header = False)
            else:    
                c_hist.to_csv(final_caste_file, index=False)
                r_hist.to_csv(final_rel_file, index=False)
            
            master_c_frame = master_c_frame.append(c_hist, ignore_index = True)
            master_r_frame = master_r_frame.append(r_hist, ignore_index = True)
            
            final_caste_file.flush()
            final_rel_file.flush()
            
        except Exception as e:
            print('Missed reading file '+file+' because of error:' + str(e))
        
        finally:
            counter = counter + 1
            os.remove(file)
   
    c_freq = master_c_frame.groupby(['Caste_Name'])['Caste_Counts'].sum()
    c_freq = c_freq.to_frame()
    file_array = ['Final_File'] * len(c_freq.index)
    c_freq.insert(0, 'PartNo', file_array)
    c_freq.insert(1, 'Caste_Name', list(c_freq.index))
    #print (c_freq.columns)
    
    c_freq.to_csv(final_caste_file, index = False, index_label = False, header = False)
    ### This file is creating some issues where the index is also getting printed out, don't know why
    
    ####
    r_freq = master_r_frame.groupby(['Religion_Name'])['Rel_Counts'].sum()
    r_freq = r_freq.to_frame()
    file_array = ['Final_File'] * len(r_freq.index)
    r_freq.insert(0, 'PartNo', file_array)
    r_freq.insert(1, 'Religion_Name', list(r_freq.index))
    
    r_freq.to_csv(final_rel_file, index = False, index_label = False, header = False)
    
    final_caste_file.close()
    final_rel_file.close()
    
    #### upload to GCP folder
    save_blob = bucket.blob('analysis/ACNo238_Caste_Allocation.csv')
    save_blob.upload_from_filename('ACNo238_Caste_Allocation.csv')
    save_blob = bucket.blob('analysis/ACNo238_Rel_Allocation.csv')
    save_blob.upload_from_filename('ACNo238_Rel_Allocation.csv')
    
    #os.remove('ACNo238_Caste_Allocation.csv')
    #os.remove('ACNo238_Rel_Allocation.csv')