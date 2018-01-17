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
    img = cv2.imread('./imgout.jpg')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gaus = cv2.GaussianBlur(gray, (3, 3), 0)
    edges = cv2.Canny(gaus, 50, 100, apertureSize=3)
    minLineLength = 20
    maxLineGap = 15
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 40, minLineLength, maxLineGap)
    for pt in zip(*loc[::-1]):

        for x1, y1, x2, y2 in lines[0]:
            if ((pt[0] + w < x1 < pt[0]+ w + 40) and (pt[1] - 12 < y1 < pt[1] + h + 18) or (pt[0] + w < x2 < pt[0]+ w + 40) and (pt[1] - 12 < y2 < pt[1] + h + 18)):
               print x1,y1,x2,y2
               if (x1<x2):
                  d1=list(pt)
                  d1[0]=d1[0]+43
                  pt=tuple(d1)
               else:
                   d2 = list(pt)
                   d2[1] = d2[1] +58
                   pt = tuple(d2)
                   cv2.rectangle(img_rgb, (pt[0] + w, pt[1] - 10), (pt[0] + w + 40, pt[1] + 12), (7, 249, 151), 2)
                   cv2.imshow('Detected', img_rgb)
                   cv2.waitKey(0)

image = ("imgout.jpg")
Target = ('tt.jpg')
value=0.96
match_img(image,Target,value)