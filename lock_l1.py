import cv2
import Image
import numpy as np


def match_t1(image_path, Target, value):
    global p1
    img_rgb = cv2.imread(image_path)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(Target, 0)
    w, h = template.shape[::-1]
    threshold = value
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res)
    p1=maxLoc
    # loc = np.where(res >= threshold)
    # for p1 in zip(*loc[::-1]):
    cv2.rectangle(img_rgb, p1, (p1[0] + w, p1[1] + h), (7, 249, 151), 2)

    cv2.imshow('Index', img_rgb)
    cv2.waitKey(0)
    return p1
    # return

image = ("imgout.jpg")
Target = ('Index_label.jpg')
value=0.75
match_t1(image,Target,value)