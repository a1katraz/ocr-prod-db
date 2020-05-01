import os
from google.cloud import storage
import pandas
import csv

if __name__ == '__main__':
    storage_client = storage.Client.from_service_account_json('/home/vishalvivek8/key.json')
    bucket = storage_client.bucket('raw_images_ocr')
    blobs = bucket.list_blobs(prefix = 'outputs/')
    cwd = os.getcwd()
    
    file = cwd+'/dict/cleanup.csv'
    
    laundry_list = pandas.read_csv(file, header = 0, sep = ',', encoding = 'utf8', error_bad_lines = False)
    
    for i in laundry_list.index:
        try:
            filename = 'FinalRoll_ACNo_' + str(laundry_list['constituency'][i]) + \
                    'PartNo_'+ str(laundry_list[' file_name'][i]) + '.csv'
            blob = bucket.blob('outputs/'+ filename)
            blob.download_to_filename(filename)
            print ("Reading File:" + filename)

            with open(filename, 'r+') as f:
                lines = f.readlines()
                f.seek(0)
                counter = 0
                for line in lines:
                    if counter != laundry_list[' line_no'][i]:
                        f.write(line)
                    counter += 1
                f.truncate()
        
            try:
                df = pandas.read_csv(filename, header = 0, sep = ',', encoding = 'utf8', error_bad_lines = False)
                blob.delete
                blob = bucket.blob('outputs/' + filename)
                blob.upload_from_filename(filename)
                
            except Exception as e:
                print('Error in reading file still '+str(e))
                continue       
                
            finally:
                os.remove(filename)

        except Exception as e:
            print('Error in looping '+str(e))