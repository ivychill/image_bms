import cv2
import Image
import numpy as np


def match_t5(image_path, Target, value):
    global p5
    img_rgb = cv2.imread(image_path)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(Target, 0)
    w, h = template.shape[::-1]
    threshold = value
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    for p5 in zip(*loc[::-1]):
        cv2.rectangle(img_rgb,  p5, (p5[0] + w, p5[1] + h), (7, 249, 151), 2)

    cv2.imshow('Rtr', img_rgb)
    cv2.waitKey(0)
    return p5
    # return
image = ("Rpi.jpg")
Target = ('l5.jpg')
value=0.85
match_t5(image,Target,value)