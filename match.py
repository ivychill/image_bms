import cv2
import Image
import numpy as np
def match_img(image_path, Target, value):
    img_rgb = cv2.imread(image_path)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(Target, 0)
    w, h = template.shape[::-1]
    threshold = value
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (7, 249, 151), 2)
    #     cv2.rectangle(img_rgb, (pt[0] + w + 40, pt[1] + h + 18), (pt[0] + w + 40+43,pt[1] + h+18+66),(7, 249, 151), 2)
    #     cv2.rectangle(img_rgb, (pt[0] + w + 40, pt[1] -10-66), (pt[0] + w + 40 + 43, pt[1] -10),(7, 249, 151), 2)
    # cv2.rectangle(img_rgb, (pt[0] + w, pt[1] - 10), (pt[0] + w + 40, pt[1] + 12), (7, 249, 151), 2)
    # cv2.rectangle(img_rgb, (pt[0] + w, pt[1] + h - 3), (pt[0] + w + 40, pt[1] + h + 18), (7, 249, 151), 2)
    # cv2.imwrite('move_image.jpg',img_rgb)
    # cv2.imwrite('l5_image.jpg',img_rgb)

    cv2.imshow('Detected', img_rgb)
    cv2.waitKey(0)

    # return img_rgb,pt,w,h
image = ("imgout.jpg")
Target = ('ttt.jpg')
value=0.9
match_img(image,Target,value)