import cv2
import numpy as np

img = cv2.imread('./1.jpg')
image=cv2.imread('./DST.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

gaus = cv2.GaussianBlur(gray, (3, 3), 0)

edges = cv2.Canny(gaus, 50, 100, apertureSize=3)
cv2.imshow('ii',edges)
minLineLength = 20
maxLineGap = 15
lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 40, minLineLength, maxLineGap)
#
#
for x1, y1, x2, y2 in lines[0]:
    cv2.line(image, (x1, y1), (x2, y2), (255,255,255), 1)

cv2.imshow('hline',image )
# cv2.imwrite('hline.jpg',image)
#


import matplotlib.pyplot as plt
# img=cv2.imread('./hline.jpg',0)
#
# ret,th1 = cv2.threshold(img,83,255,cv2.THRESH_BINARY)
# th2 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,7,2)
# th3 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,9,2)
# images = [img,th1,th2,th3]
# plt.figure()
# for i in xrange(4):
#     plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
# plt.show()
# ret2,th2 = cv2.threshold(img,80,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

# cv2.imshow('th2.jpg',th1)
# cv2.imwrite('th2.jpg',th1)
# img = cv2.imread('./hline.jpg')
#
#
# lower = np.array([0, 0, 255 ],dtype="uint8")
# upper = np.array([100, 100, 255], dtype="uint8")
#
#                 # find the colors within the specified boundaries and apply the mask
# mask = cv2.inRange(img, lower, upper)
# cv2.imshow('mask',mask)

# img = cv2.imread('./1.jpg')
# mask = cv2.imread('hline.jpg',0)
# dst = cv2.inpaint(img,mask,2,cv2.INPAINT_TELEA)
# #
# cv2.imshow('dst',dst)
# cv2.imwrite('DST.jpg',dst)
cv2.waitKey(0)
cv2.destroyAllWindows()











# kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(2, 2))
#
# eroded = cv2.erode(img,kernel,iterations = 1)
#
# dilated = cv2.dilate(eroded,kernel,iterations = 3)
#
# erod = cv2.erode(dilated,kernel,iterations = 2)
#
#
#
#
# cv2.imshow("houghline", dilated)
# cv2.imshow("hough", erod)

# dilated = np.array(dilated)
# cv2.imwrite('line.jpg',dilated)
cv2.waitKey()
cv2.destroyAllWindows()

# img =cv2.imread('./3.jpg',0)
# ret,thresh1 = cv2.threshold(img,50,255,cv2.THRESH_BINARY)
# cv2.imwrite('th.jpg',thresh1)
# image =cv2.imread('./th.jpg')
#
#
# kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
# #
#
# # opening = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
#
# dilation = cv2.dilate(image,kernel,iterations = 3)
#
#
# # cv2.imwrite('op.jpg',opening)
# cv2.imwrite('DD2.jpg',dilation)
#
# erosion = cv2.erode(dilation,kernel,iterations = 3)
# cv2.imwrite('EE.jpg',erosion)

# cv2.imshow('D',dilation)
