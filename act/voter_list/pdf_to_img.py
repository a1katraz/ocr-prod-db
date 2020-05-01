#!/usr/bin/python
# -*- coding: utf-8 -*-
import PyPDF2
from PIL import Image
from google.cloud import storage
from img_to_names import convert_to_names
import os

if __name__ == '__main__':

    storage_client = storage.Client.from_service_account_json('/home/vishalvivek8/key.json')

    bucket = storage_client.bucket('raw_images_ocr')

    blobs = bucket.list_blobs(prefix='docs/')
    
    cwd = os.getcwd()
    #print(len(blobs))
    for blob in blobs:
        if(blob.name == 'docs/' or 'prcs_cmpl' in blob.name):
            #print (blob.name)
            continue

        print ('Processing Voter Raw File : ' + blob.name.replace('docs/', ''))

        blob.download_to_filename(cwd + '/docs/' + blob.name.replace('docs/', ''))

        filepath = cwd + '/docs/' + blob.name.replace('docs/', '')

        input1 = PyPDF2.PdfFileReader(open(filepath, 'rb'))

        for x in range(0, input1.getNumPages()):
            if x == 1:
                continue

            page0 = input1.getPage(x)
            xObject = page0['/Resources']['/XObject'].getObject()
            for obj in xObject:
                if xObject[obj]['/Subtype'] == '/Image':
                    size = (xObject[obj]['/Width'],
                            xObject[obj]['/Height'])
                    data = xObject[obj].getData()
                if xObject[obj]['/ColorSpace'] == '/DeviceRGB':
                    mode = 'RGB'
                else:
                    mode = 'P'

                if xObject[obj]['/Filter'] == '/FlateDecode':
                    img = Image.frombytes(mode, size, data)
                    img.save(cwd + '/images/voter_list/' + obj[1:] + '.png')

        conversion_name = convert_to_names(blob.name.replace('docs/', '').replace('.pdf', ''))

        # ## Save output file to gcp

        #save_bucket = storage_client.bucket('raw_images_ocr')
        save_blob = bucket.blob('outputs/'+blob.name.replace('docs/', '').replace('pdf', 'csv'))
        save_blob.upload_from_filename(conversion_name)
        bucket.rename_blob(blob, blob.name.replace('.pdf', '_prcs_cmpl.pdf'))

        # ###cleanup actions

        os.remove(filepath)
        save_blob.upload_from_filename(conversion_name)
        os.remove(conversion_name)
