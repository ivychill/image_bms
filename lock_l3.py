import cv2
import Image
import numpy as np


def match_t3(image_path, Target, value):
    global p3
    img_rgb = cv2.imread(image_path)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(Target, 0)
    w, h = template.shape[::-1]
    threshold = value
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res)
    p3 = maxLoc
    # loc = np.where(res >= threshold)
    # for p3 in zip(*loc[::-1]):
    cv2.rectangle(img_rgb,  p3, (p3[0] + w, p3[1] + h), (7, 249, 151), 2)

    cv2.imshow('Raero', img_rgb)
    cv2.waitKey(0)
    return p3
    # return
image = ("Rtr.jpg")
Target = ('lock_label.jpg')
value=0.99
match_t3(image,Target,value)