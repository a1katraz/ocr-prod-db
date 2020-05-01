#!/usr/bin/python
# -*- coding: utf-8 -*-
import io
from PIL import Image
import os
from bord import find_boxes
import pytesseract
import argparse
import os
import re
import cv2


def clean_up(text):
    return text.replace('।', '1').replace('"', '-').replace('"', '').replace(',', ';')
    

def get_names_cv(filepath, serial, appendix_page):
    cwd = os.path.abspath(os.getcwd())

    print ('Reading file:' + filepath.split('/')[-1])
    im = Image.open(filepath)

    # #### Get Election Type and  Constituency Name
    # try:
    # ....im = Image.open(filepath)
    # ....crop_rectangle = (40, 10, 600, 40)
    # ....im_crop = im.crop(crop_rectangle)....
    # ....texts = pytesseract.image_to_string(im_crop, lang='hin')

    # ....election_name = ''
    # ....constituency_name = ''
    # ....if (len(texts) > 0 and ':' in texts):
    # ........election_name = texts.split(",")[0].strip()
    # ........constituency_name = texts.split(":")[1].strip()
    # except:
    # ....election_name = 'ERROR'
    # ....constituency_name = 'ERROR'
    # ....pass

    ###Get Header Address
    try:
       major_address = ''
       if(appendix_page == 0):
          crop_rectangle = (40, 50, 500, 72)
          im_crop = im.crop(crop_rectangle)
          (w, h) = im_crop.size
          im_add_mag = im_crop.resize((w * 3, h * 5), Image.ANTIALIAS)
          texts = pytesseract.image_to_string(im_add_mag, lang='hin', config = '--psm 7')
          #print(texts)
          if (len(texts) > 0 and ':' in texts):
              major_address = texts.split(":")[2].strip().replace(',', '-') #................# dont' read anything apart from the first line
          major_address = clean_up(major_address)
          #print(major_address)
    except:
       major_address = 'ERROR'
       pass

    # #### Get Part Number
    # try:
    # ....crop_rectangle = (990, 10, 1130, 35)
    # ....im_crop = im.crop(crop_rectangle)
    # ....#im_crop.show()
    # ....w, h = im_crop.size
    # ....im_crop_mag = im_crop.resize((w*3, h*5), Image.ANTIALIAS)
    # ....texts = pytesseract.image_to_string(im_crop_mag, lang='eng', \
    # ........................................config='--psm 7 -c tessedit_char_whitelist=0123456789')
    #
    # ....part_number = ''
    # ....part_number = texts.strip()
    # ....print (part_number)
    # except:
    # ....part_number = 'ERROR'
    # ....pass

    # ###Get Voter Details

    counter = 1
    (boxes, appendix_page) = find_boxes(filepath, appendix_page)
    outcomes = list()
    prev_serial = serial - 1

    # print (prev_serial)

    for box in boxes:
        #print('Reading voter counter: ' + str(counter))
        try:
            crop_rectangle = (box[0], box[1], box[2], box[3])
            im_crop = im.crop(crop_rectangle)
            #im_crop.save(cwd + '/tmp/app_' + str(counter) + '.png')

                # ##Get Serial No

            if appendix_page == 0:
                crop_rectangle = (7, 2, 80, 20)
            else:
                crop_rectangle = (7, 6, 82, 29)
            im_serial = im_crop.crop(crop_rectangle)
            (w, h) = im_serial.size
            im_serial_mag = im_serial.resize((w * 3, h * 5),
                    Image.ANTIALIAS)
            texts = pytesseract.image_to_string(im_serial_mag,
                    lang='eng',
                    config='--psm 7 -c tessedit_char_whitelist=0123456789ES'
                    )
            serial_num = texts.strip()
            if(serial_num.startswith('E') or serial_num.startswith('S')):
                continue
                #this serial number has been deleted and we need to pass this
            if (not serial_num.isdigit() or int(serial_num) != prev_serial + 1):
                serial_num = str(prev_serial + 1)

                # print ("Serial Number is:" + serial_num)

                # ## Get Name and Father's Name

            if appendix_page == 0:
                crop_rectangle = (4, 21, 269, 136)
            else:
                crop_rectangle = (7, 30, 275, 140)
            im_main = im_crop.crop(crop_rectangle)
            #im_main.save(cwd + '/tmp/app_main' + str(counter) + '.png')

            texts = pytesseract.image_to_string(im_main, lang='hin')
            lines = texts.split('\n')

            for linex in lines:
                if linex.strip() == '':
                    lines.remove(linex)

            voter_det = ['', '', '', '', '']
            voter_det[0] = lines[0].split(':')[1].strip()  # name
            voter_det[0] = clean_up(voter_det[0])
            
            if(':' in lines[1]):
                voter_det[1] = lines[1].split(':')[1].strip()  # father's name
            else:
                voter_det[0] = voter_det[0] + ' ' + lines[1].strip() #name extended to more than 1 line
                voter_det[1] = lines[2].split(':')[1].strip()  # father's name
                
            voter_det[1] = clean_up(voter_det[1])
            
                # ####Get House No

            if appendix_page == 0:
                crop_rectangle = (59, 48, 100, 65)
            else:
                crop_rectangle = (65, 48, 110, 65)
            im_house = im_main.crop(crop_rectangle)
            (w, h) = im_house.size

                # Blow up image to get the characters clearly

            im_house_mag = im_house.resize((w * 5, h * 5),
                    Image.BICUBIC)

                # im_house_mag.show()

            texts = pytesseract.image_to_string(im_house_mag, lang='eng',
                    config='--psm 7 -c tessedit_char_whitelist=0123456789'
                    )
            voter_det[2] = texts.strip()  # house no
            voter_det[2] = clean_up(voter_det[2])

                # print ('House No:' + texts)

                # ####Get Age

            if appendix_page == 0:
                crop_rectangle = (32, 66, 55, 85)
            else:
                crop_rectangle = (34, 68, 60, 90)
            im_age = im_main.crop(crop_rectangle)
            (w, h) = im_house.size

                # Blow up image to get the characters clearly

            im_age_mag = im_age.resize((w * 3, h * 5), Image.BICUBIC)

                # im_age_mag.show()

            texts = pytesseract.image_to_string(im_age_mag, lang='eng',
                    config='--psm 7 -c tessedit_char_whitelist=0123456789'
                    )
            voter_det[3] = texts.strip()  # age

                # print('Age: '+texts)

                # ####Get Gender

            if appendix_page == 0:
                crop_rectangle = (95, 65, 170, 88)
            else:
                crop_rectangle = (95, 65, 170, 90)
            im_gender = im_main.crop(crop_rectangle)

                # im_gender.show()
                # im_gender_mag = im_gender.resize((w*3, h*3), Image.BILINEAR)

            texts = pytesseract.image_to_string(im_gender, lang='hin',
                    config='--psm 7')
            voter_det[4] = texts.strip()  # gender
            if voter_det[4].startswith('\xe0\xa4\xaa'):
                voter_det[4] = \
                    '\xe0\xa4\xaa\xe0\xa5\x81\xe0\xa4\xb0\xe0\xa5\x82\xe0\xa4\xb7'

                # print('Gender: ' + texts)........

                # #####Address Correction for special characters:

            voter_det[2] = voter_det[2].replace('\xe0\xa5\xa4', '1')
            voter_det[2] = voter_det[2].replace('\xe0\xa5\xa5', '11')

                # ####Voter Card

            if appendix_page == 0:
                crop_rectangle = (150, 1, 372, 25)
            else:
                crop_rectangle = (185, 4, 375, 25)
            im_code = im_crop.crop(crop_rectangle)
            (w, h) = im_code.size
            im_code_mag = im_code.resize((w * 2, h * 2), Image.BICUBIC)
            texts = pytesseract.image_to_string(im_code_mag, lang='eng')

                # print (texts)

            voter_card = ''
            error_switch = 'FALSE'
            if len(texts) > 0:
                voter_card = re.sub(r"[^a-zA-Z0-9]+", '/',
                                    texts.strip()).lstrip('1234567890,.'
                        ).rstrip('/')
            if voter_card.startswith('BR/') and len(voter_card) >= 16:
                voter_card = voter_card
            elif len(voter_card) >= 10:
                voter_card = voter_card
            else:
                voter_card = voter_card + '_ERROR'

            if voter_card.endswith('_ERROR'):
                error_switch = 'TRUE'

                # ###Voter's surname is person's last name if male or father's last name if not male

            voter_surname = ''
            if voter_det[4] \
                == '\xe0\xa4\xaa\xe0\xa5\x81\xe0\xa4\xb0\xe0\xa5\x82\xe0\xa4\xb7':
                if len(voter_det[0].split(' ')) > 1:
                    voter_surname = voter_det[0].split(' ')[-1]
            else:
                if len(voter_det[1].split(' ')) > 1:
                    voter_surname = voter_det[1].split(' ')[-1]
                    
            voter_surname = clean_up(voter_surname)

            if error_switch == 'FALSE':  # Don't write this data if Voter Card Information has an error
                single_tuple = list()
                single_tuple.extend((
                    serial_num,
                    voter_card,
                    voter_det[0],
                    voter_det[1],
                    voter_det[3],
                    voter_det[4],
                    voter_det[2],
                    major_address,
                    voter_surname,
                    '',
                    '',
                    error_switch,
                    ))
                outcomes.append(single_tuple)
        except Exception as e:

            # pass

            print ('Error in reading voter details for:' + str(counter) \
                + ' Error:' + str(e))
        finally:

            prev_serial = serial
            counter = counter + 1
            serial = serial + 1

    return (outcomes, counter - 1, appendix_page)
