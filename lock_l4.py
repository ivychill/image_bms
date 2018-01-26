import cv2
import Image
import numpy as np


def match_t4(image_path, Target, value):
    global p4
    img_rgb = cv2.imread(image_path)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(Target, 0)
    w, h = template.shape[::-1]
    threshold = value
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    for p4 in loc[::-1]:
        for p4 in loc[::-1]:
            if loc[0][:-1]>220:


                print p4
                cv2.rectangle(img_rgb, p4, (p4[0] + w, p4[1] + h), (7, 249, 151), 2)
                cv2.imshow('Rpi', img_rgb)
                cv2.waitKey(0)
                return p4



    # for p4 in zip(*loc[::-1]):




    # return p4
    # return
image = ("./imgout.jpg")
Target = ('Rpi_label.jpg')
value=0.85
match_t4(image,Target,value)