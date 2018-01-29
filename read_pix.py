import cv2
import os
import pytesseract
import Image
import re

pt_miss_clock=(383,124)
wide_miss_clock=28
heigh_miss_clock=22
image = Image.open('./imgout_Lmfd.jpg')
box_miss_clock = (pt_miss_clock[0], pt_miss_clock[1], pt_miss_clock[0] + wide_miss_clock, pt_miss_clock[1] + heigh_miss_clock)
region_miss_clock = image.crop(box_miss_clock)
# print region_miss_clock
# if region_miss_clock is None:
# if format(region_miss_clock) is not None:
miss_clock_digit = pytesseract.image_to_string(region_miss_clock, config='--psm 7')
# print type(miss_clock_digit)
#
# print miss_clock_digit.isdigit(miss_clock_digit)
#
# if miss_clock_digit > 0:
#     print miss_clock_digit
# else:
#     miss_clock_digit = None
# miss_clock_digit=re.match('^?\d{1,2}$', miss_clock_digit)

sss = str(miss_clock_digit)
print sss
if sss ==',':
   miss_clock_digit = None
   print len(miss_clock_digit)
else:
    print len(miss_clock_digit)



