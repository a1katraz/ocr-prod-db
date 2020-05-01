#!/usr/bin/env python
# coding: utf-8

# In[19]:


import PyPDF2
from PIL import Image
from google.cloud import storage
import os
import re
from pathlib import Path

if __name__ == '__main__':

    storage_client = storage.Client.from_service_account_json('/home/vishalvivek8/key.json')
    bucket = storage_client.bucket('raw_images_ocr')
    blobs = bucket.list_blobs(prefix='docs/form_20/')
    
    cwd = os.getcwd()
    for blob in blobs:
        if(blob.name == 'docs/form_20/' or 'prcs_cmpl' in blob.name):
            continue

        print ('Processing Form 20 File : ' + blob.name.replace('docs/form_20/', ''))
        blob.download_to_filename(str(Path(cwd)) + '/docs/form_20/' + blob.name.replace('docs/form_20/', ''))
        filepath = str(Path(cwd)) + '/docs/form_20/' + blob.name.replace('docs/form_20/', '')

        input1 = PyPDF2.PdfFileReader(open(filepath, 'rb'))     
        file_names = list()
        
        for x in range(0, input1.getNumPages()):        
            page0 = input1.getPage(x)
            xObject = page0['/Resources']['/XObject'].getObject()
            for obj in xObject:
                if xObject[obj]['/Subtype'] == '/Image':
                    size = (xObject[obj]['/Width'], xObject[obj]['/Height'])
                    if xObject[obj]['/Filter'] == '/DCTDecode':         #DCTDecode implementation is slightly different
                        data = xObject[obj]._data
                    else:
                        data = xObject[obj].getData()
                    
                    if xObject[obj]['/ColorSpace'] == '/DeviceRGB':
                        mode = 'RGB'
                    else:
                        mode = 'P'
                    
                    if(obj[1:] in file_names):
                        last_name = file_names[-1]
                        last_cnt = int(re.search(r'\d+', last_name).group(0))
                        last_cnt += 1
                        name = re.search(r'[a-zA-Z]+', last_name).group(0) + str(last_cnt)
                    else:
                        name = obj[1:]
                    file_names.append(name)
                    
                    if xObject[obj]['/Filter'] == '/FlateDecode':
                        img = Image.frombytes(mode, size, data)
                        img.save(str(Path(cwd)) + '/images/form_20/' + name + '.png')
                    elif xObject[obj]['/Filter'] == '/DCTDecode':
                        img = open(str(Path(cwd)) + '/images/form_20/' + name + ".jpg", "wb")
                        img.write(data)
                        img.close()
                    elif xObject[obj]['/Filter'] == '/JPXDecode':
                        img = open(str(Path(cwd)) + '/images/form_20/' + name + ".jp2", "wb")
                        img.write(data)
                        img.close()
    
    ## Images created - start processing
    print('abc')


# In[ ]:




