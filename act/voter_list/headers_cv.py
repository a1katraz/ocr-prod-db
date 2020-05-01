#!/usr/bin/python
# -*- coding: utf-8 -*-
from PIL import Image
import os
from bord import find_boxes
import pytesseract
import argparse
import os
import re
import cv2


def get_headers(header_filepath):
    cwd = os.path.abspath(os.getcwd())
    print('Reading Header file:' + header_filepath.split('/')[-1])

    im = Image.open(header_filepath)
    output = list()

    try:

        # #### Get Election Year

        crop_rectangle = (345, 270, 435, 290)
        im_ele_year = im.crop(crop_rectangle)

        texts = pytesseract.image_to_string(im_ele_year, lang='eng',
                config='--psm 7 -c tessedit_char_whitelist=0123456789')

        election_year = ''
        if len(texts) > 0:
            election_year = texts.strip().replace(',', '')
        output.append(election_year)
    except:
        pass
        output.append('')

    try:

        # #### Get Assembly Constituency Name and Details

        crop_rectangle = (61, 89, 940, 145)
        im_ac = im.crop(crop_rectangle)

        texts = pytesseract.image_to_string(im_ac, lang='hin',
                config='--psm 7')

        assembly_constituency_name = ''
        assembly_constituency_number = ''
        assembly_constituency_reservation = ''
        if len(texts) > 0 and ':' in texts:
            assembly_constituency_name = texts.split(':')[2].strip().replace(',', ';')
            assembly_constituency_number = \
                assembly_constituency_name.split('-')[0].strip().replace(',', '')
            assembly_constituency_reservation = \
                assembly_constituency_name.split('-')[1].split(' '
                    )[2].strip().replace(',', '')
        output.extend((assembly_constituency_name,
                      assembly_constituency_number,
                      assembly_constituency_reservation))
    except:
        pass
        output.extend(('', '', ''))

    try:

        # #### Get Parliamentary Constituency Name and Details

        crop_rectangle = (61, 155, 945, 200)
        im_pc = im.crop(crop_rectangle)

        texts = pytesseract.image_to_string(im_pc, lang='hin',
                config='--psm 7')

        parliament_constituency_name = ''
        parliament_constituency_number = ''
        parliament_constituency_reservation = ''
        if len(texts) > 0 and ':' in texts:
            parliament_constituency_name = texts.split(':')[2].strip().replace(',', ';')
            parliament_constituency_number = \
                parliament_constituency_name.split('-')[0].strip().replace(',', '')
            parliament_constituency_reservation = \
                parliament_constituency_name.split('-')[1].split(' '
                    )[2].strip().replace(',', '')
        output.extend((parliament_constituency_name,
                      parliament_constituency_number,
                      parliament_constituency_reservation))
    except:
        pass
        output.extend(('', '', ''))

    try:

        # #### Get Part No

        crop_rectangle = (1010, 115, 1090, 145)
        im_part = im.crop(crop_rectangle)

        texts = pytesseract.image_to_string(im_part, lang='eng',
                config='--psm 7 -c tessedit_char_whitelist=0123456789')

        part_number = ''
        if len(texts) > 0:
            part_number = texts.strip().replace(',', '')
        output.append(part_number)
    except:
        pass
        output.append('')

    try:

        # #### Get EPRPD

        crop_rectangle = (300, 425, 500, 450)
        im_publish = im.crop(crop_rectangle)

        texts = pytesseract.image_to_string(im_publish, lang='eng',
                config='--psm 7 -c tessedit_char_whitelist=0123456789-')

        publish_date = ''
        if len(texts) > 0:
            publish_date = texts.strip().replace(',', '')
        output.append(publish_date)
    except:
        pass
        output.append('')

    try:

        # #### Get Booth Details

        crop_rectangle = (60, 1035, 615, 1070)
        im_booth = im.crop(crop_rectangle)

        texts1 = pytesseract.image_to_string(im_booth, lang='hin')
        texts2 = pytesseract.image_to_string(im_booth, lang='eng',
                config='--psm 7 -c tessedit_char_whitelist=0123456789')

        booth_name = ''
        booth_num = ''
        if len(texts) > 0:
            booth_name = texts1.strip().replace(',', ';')
            booth_num = texts2.strip().replace(',', '')
        output.extend((booth_name, booth_num))
    except:
        pass
        output.extend(('', ''))

    try:

        # #### Get PIN  Code

        crop_rectangle = (810, 790, 910, 805)
        im_pin = im.crop(crop_rectangle)

        texts = pytesseract.image_to_string(im_pin, lang='eng',
                config='--psm 7 -c tessedit_char_whitelist=0123456789')

        pin_code = ''
        if len(texts) > 0:
            pin_code = texts.strip().replace(',', '')
        output.append(pin_code)
    except:
        pass
        output.append('')

    # print (output)

    return output
