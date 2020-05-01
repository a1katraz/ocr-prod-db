import os
from google.cloud import storage
import pandas
import re

def get_names_order(filename):
	return int(filename.split('.')[0].split('_')[3])

def match_part_number(part_number, part_number_file):
	##print ('Processing Serial Number: ' + serial_num)
	return part_number_file


if __name__ == '__main__':
	storage_client = storage.Client.from_service_account_json('/home/vishalvivek8/key.json')
	bucket = storage_client.bucket('raw_images_ocr')
	blobs = bucket.list_blobs(prefix = 'outputs/')
	cwd = os.getcwd()
	
	output_files = list()
	
	for blob in blobs:
		if(blob.name == 'outputs/' or blob.name.startswith('outputs/ACNo')):
			continue
		output_files.append(blob.name.replace('outputs/', ''))
    
	output_files.sort(key = get_names_order)
	
	final_file = open('ACNo238_CombinedFile.csv', 'w+')
	
	counter = 1

	for file in output_files:
		try:
			blob = bucket.blob('outputs/'+file)
			blob.download_to_filename(file)
			print ("Reading File:" + file)
			df = pandas.read_csv(file, header = 0, sep = ',', encoding = 'utf8', error_bad_lines = False)
			part_number_final = file.split('.')[0].split('_')[3]
			
			df['Part No.'] = part_number_final
			
			if (counter == 1):
				df.to_csv(final_file, header = True, encoding = 'utf-8-sig', index = False)
			else:
				df.to_csv(final_file, header = False, encoding = 'utf-8-sig', index = False)
			
			final_file.flush()
		
		except pandas.errors.ParserError as e:
			error_line = str(e)
			i = int(re.findall(r'\d+', error_line)[0])
			if(i <= len(df.index)):  
				df.drop(df.index[i])
			if(counter == 1):
				df.to_csv(final_file, header = True, encoding = 'utf-8-sig', index = False)
			else:
				df.to_csv(final_file, header = False, encoding = 'utf-8-sig', index = False)
			
			final_file.flush()
	
		except Exception as e:
			print('Missed reading file '+file+' because of error:' + str(e))

		finally:
			counter = counter + 1
			os.remove(file)
	
	final_file.close()
	
	### Save File to GCP
	save_blob = bucket.blob('outputs/ACNo238_CombinedFile.csv')
	save_blob.upload_from_filename('ACNo238_CombinedFile.csv')

	### Cleanup
	#os.remove(final_file)



