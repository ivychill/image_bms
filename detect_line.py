import cv2
# def detect_line(image):
# image = cv2.imread('./1.jpg')
# box = (20,50,60,90)
# region = image.crop(box)
# region.show()
# cv2.waitKey(3)
#     # return region
# region.save('Re.jpg')


# contour=cv2.imread('region.jpg')
# measure_dist=0
#
# img = cv2.imread('./1.jpg')
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# gaus = cv2.GaussianBlur(gray, (3, 3), 0)
# edges = cv2.Canny(gaus, 50, 100, apertureSize=3)
# # cv2.imshow('ii',edges)
# minLineLength = 20
# maxLineGap = 15
# lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 40, minLineLength, maxLineGap)
# for at in lines[0]:
#     cv2.PointPolygonTest(contour, at, measure_dist)
