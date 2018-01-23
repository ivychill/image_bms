#!/usr/bin/env python
# encoding: utf-8
'''
@author: qingyao.wang
@license: (C) Copyright 2017-2020, kuang-chi Corporation Limited.
@contact: qingyao.wang@kuang-chi.com
@file: imageClinet.py
@time: 2018-01-05 14:54
@desc:
'''
import Image
from log_config import *
import time
from bms_interface import *
#from bitmap import BitMap
import os
import sys
# import io,numpy
# import requests
from PIL import Image
from io import BytesIO
import numpy as np
import cv2
import pytesseract
import base64
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True


# global s #全局



class ImageProcessor:
    def __init__(self):
        self.bms = BmsInterface()
    def rec_main(self):
        # self.getImage("mfdleft")
        while True:
            time.sleep(2)
            if self.getImage("mfdleft"):
                valid = self.getImage("mfdleft")
                if valid==False:
                    continue

                self.match_enemy()
                # pt_td,wide_td,height_td = self.match_td()
                pt_td=self.match_td()
                if pt_td:

                        # line=self.detect_td_line(pt_td, wide_td, height_td)
                    line = self.detect_td_line(pt_td)
                    if line==0:
                        self.move_td()
                        continue

                    else:
                        self.process_td(pt_td)


                    # self.process_td(pt_td, wide_td, height_td)


    def getImage(self, msg):

        self.bms.image_socket.send(msg)
        stringData = self.bms.image_socket.recv(1024*1024)
        aa = len(stringData)
        # print aa
        if len(stringData) > 0:
            hex_data=  base64.b64decode(stringData) #base64解码图片
            leidaimg = open('imgout.bmp', 'wb')
            leidaimg.write(hex_data)
            leidaimg.close()
            valid=True
            # try:
            #     Image.open('imgout.bmp').verify()
            # os.system("for i in *.bmp;do convert ${i} ${i%bmp}jpg;done")
            try:
                os.system("convert imgout.bmp imgout.jpg")
            except OSError:
                valid =False
                print 'wwwwwww'
            # time.sleep(0.5)
        return valid



        # logger.debug('valid: %s' % valid)



        # self.bms.image_socket.close()
        # img_rgb = cv2.imread('imgout.jpg')
        # self.img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)


    def match_enemy(self,value=0.9):
        img_rgb=cv2.imread('./imgout.jpg')
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        Target=cv2.imread('./t4.jpg')
        template = cv2.cvtColor(Target, cv2.COLOR_BGR2GRAY)
        wide, height = template.shape[::-1]
        self.value=value
        threshold = value
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        # if not loc:
        #     return -1
        # else:
            # self.enemy_left = pt
        if loc:
            for pt in zip(*loc[::-1]):
               cv2.rectangle(img_rgb, pt, (pt[0] + wide, pt[1] + height), (7, 249, 151), 2)
               cv2.rectangle(img_rgb, (pt[0] + wide, pt[1] - 4), (pt[0] + wide + 40, pt[1] + 19), (7, 249, 151), 2)
               cv2.rectangle(img_rgb, (pt[0] + wide, pt[1] + height - 1), (pt[0] + wide + 40, pt[1] + wide + 24), (7, 249, 151), 2)
               # cv2.imshow('Detected', img_rgb)
               # cv2.waitKey(20)
               self.enemy_pt=pt
               logger.debug('self.enemy_pt: %s' % (self.enemy_pt))
        else:
            return None

        # sys.exit(0)

    def match_td(self, value=0.7):
        img_rgb = cv2.imread('./imgout.jpg')
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        Target = cv2.imread('./ttt.jpg')
        template = cv2.cvtColor(Target, cv2.COLOR_BGR2GRAY)
        wide_td, height_td = template.shape[::-1]
        self.wide_td=wide_td
        self.height_td=height_td
        self.value = value
        threshold = value
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)

        # if not loc:
        #     return -1
        # else:
        if loc:
            for pt_td in zip(*loc[::-1]):
                cv2.rectangle(img_rgb, pt_td, (pt_td[0] + wide_td, pt_td[1] + height_td), (7, 249, 151), 2)
                cv2.rectangle(img_rgb, (pt_td[0] + wide_td, pt_td[1] -4), (pt_td[0] + wide_td + 40, pt_td[1] + 19), (7, 249, 151), 2)
                cv2.rectangle(img_rgb, (pt_td[0] + wide_td, pt_td[1] + height_td - 1), (pt_td[0] + wide_td + 40, pt_td[1] + height_td + 24), (7, 249, 151), 2)
                # cv2.imshow('Detected', img_rgb)
                # # cv2.imwrite('Detected',img_rgb)
                # cv2.waitKey(0)
                # return pt_td,wide_td,height_td
                return pt_td
        else:
            return None



    # def detect_td_line(self,pt_td,wide_td, height_td):
    def detect_td_line(self, pt_td):

        img_rgb = cv2.imread('./imgout.jpg')
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        gaus = cv2.GaussianBlur(img_gray, (3, 3), 0)
        edges = cv2.Canny(gaus, 50, 100, apertureSize=3)
        minLineLength = 20
        maxLineGap = 15
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 40, minLineLength, maxLineGap)
        # print self.wide_td,self.height_td
        for x1, y1, x2, y2 in lines[0]:
            # if ((pt_td[0] + wide_td < x1 < pt_td[0] + wide_td + 40) and (pt_td[1] - 4 < y1 < pt_td[1] + height_td + 19) or (
            #                     pt_td[0] + wide_td < x2 < pt_td[0] + wide_td + 40) and (pt_td[1] - 4 < y2 < pt_td[1] + height_td  + 24)):
            if ((pt_td[0] + self.wide_td < x1 < pt_td[0] + self.wide_td + 40) and (
                        pt_td[1] - 4 < y1 < pt_td[1] + self.height_td + 24) or (
                               pt_td[0] + self.wide_td < x2 < pt_td[0] + self.wide_td + 40) and (pt_td[1] - 4 < y2 < pt_td[1] + self.height_td  + 24)):

                return 0
            else:
                continue





    def move_td(self):
        self.bms.command_socket.sendto("K:101", self.bms.command_addr)
        self.bms.command_socket.sendto("K:103", self.bms.command_addr)
        logger.debug('command: %s'% ('K:101','K:103'))

    # def process_td(self,pt_td,wide_td, height_td):
    def process_td(self, pt_td):
        image = Image.open('./imgout.jpg')
        # image = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        # box1 = (pt_td[0] + wide_td, pt_td[1] -4, pt_td[0] + wide_td + 40, pt_td[1] + 19)
        # box2 = (pt_td[0] + wide_td, pt_td[1] + height_td - 1 ,pt_td[0] + wide_td + 40, pt_td[1] + height_td + 24)
        box1 = (pt_td[0] + self.wide_td, pt_td[1] - 4, pt_td[0] + self.wide_td + 40, pt_td[1] + 19)
        box2 = (pt_td[0] + self.wide_td, pt_td[1] + self.height_td - 1, pt_td[0] + self.wide_td + 40, pt_td[1] + self.height_td + 24)
        region1 = image.crop(box1)
        region2 = image.crop(box2)
        # region2.save('region2.jpg')
        # region1.show()
        # region2.show()
        # cv2.waitKey(0)
        high = pytesseract.image_to_string(region1, config='--psm 7 -c tessedit_char_whitelist=-0123456789')
        low = pytesseract.image_to_string(region2, config='--psm 7 -c tessedit_char_whitelist=-0123456789')
        print("high: %s, low: %s" % (high, low))
        # print(" low: %s" % (low))
        # region1.show()
        # region2.show()

        # region1.save("high.jpg")
        # region2.save("low.jpg")
        self.td_left,self.td_high,self.td_low=pt_td,high,low
        logger.debug('self.td_left: %s, self.td_high:%s, self.td_high:%s' % (self.td_left,self.td_high,self.td_low))
        # print self.td_left,self.td_high,self.td_low
        # self.td_left=pt_td
    # def get_td(self):
    #     return self.pt_td
    #
    # def get_enemy_coord(self):
    #     return self.pt
