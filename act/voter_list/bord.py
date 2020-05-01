#!/usr/bin/python
# -*- coding: utf-8 -*-
import cv2
import numpy as np
import os
import PIL
import math


def find_boxes(filepath, appendix_page):
    cwd = os.path.abspath(os.getcwd())

    # root = tk.Tk()
    # root.withdraw()
    # filepath = filedialog.askopenfilename()

    # print(cwd)

    image = PIL.Image.open(filepath, 'r').convert('1')
    (width, height) = image.size

    # vert_line = PIL.Image.new('1', (1, height))
    # vert_line = vert_line.save(cwd+'/gvis/images/vertical.bmp')

    vline = cv2.imread(cwd + '/images/comp/vertical.bmp')

    # hor_line = PIL.Image.new('1', (width, 1))
    # hor_line = hor_line.save(cwd+'/gvis/images/horizontal.bmp')

    hline = cv2.imread(cwd + '/images/comp/horizontal.bmp')

    x_list = list()
    y_list = list()

    x_points = list()
    y_points = list()

    min_x_index = 0
    min_x_val = height

    max_x_index = width - 1
    max_x_val = height

    for x in range(0, width, 1):
        crop_rect = (x, 0, x + 1, height)
        img_vl = image.crop(crop_rect)
        img_vl = img_vl.save(cwd + '/tmp/img_vl.bmp')
        i_line = cv2.imread(cwd + '/tmp/img_vl.bmp')
        diff = cv2.subtract(i_line, vline)
        (b, g, r) = cv2.split(diff)
        x_list.append(cv2.countNonZero(b))

        # if(cv2.countNonZero(b) < 300):
        # ....x_points.append(x)

    for x in range(0, 70):
        if min_x_val > x_list[x]:
            min_x_index = x
            min_x_val = x_list[x]

    for x in range(width - 1, width - 100, -1):
        if max_x_val > x_list[x]:
            max_x_index = x
            max_x_val = x_list[x]

    for x in range(min_x_index - 1, max_x_index):
        if x_list[x] <= math.ceil(min_x_val / 100.0) * 100:
            x_points.append(x)
    x_points.append(max_x_index)

    # print(min_x_index, min_x_val, max_x_index, max_x_val, x_points)

    for y in range(0, height, 1):
        crop_rect = (0, y, width, y + 1)
        img_vl = image.crop(crop_rect)
        img_vl = img_vl.save(cwd + '/tmp/img_hz.bmp')
        i_line = cv2.imread(cwd + '/tmp/img_hz.bmp')
        diff = cv2.subtract(i_line, hline)
        (b, g, r) = cv2.split(diff)
        y_list.append(cv2.countNonZero(b))
        if y < 1500:
            if cv2.countNonZero(b) < 200:
                y_points.append(y)
        else:
            if cv2.countNonZero(b) < 500:
                y_points.append(y)

    # print(y_points)

    boxes = list()

    for j in range(len(y_points) - 1):
        for i in range(len(x_points) - 1):
            if x_points[i + 1] - x_points[i] > 5 and y_points[j + 1] \
                - y_points[j] > 5:
                box = list()
                box.extend((x_points[i], y_points[j], x_points[i + 1],
                           y_points[j + 1]))
                boxes.append(box)

    # for box in boxes:
    # ....print('{}, {}, {}, {}'.format(box[0], box[1], box[2], box[3]))
    try:
        if( appendix_page == 0 and y_points[0] >= 110):
            appendix_page = 1
    except Exception as e:
         print('Exception happened in border processing: '+str(e))

    return (boxes, appendix_page)
