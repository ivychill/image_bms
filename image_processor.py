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
import os
from PIL import Image
import numpy as np
import cv2
import pytesseract
import base64
from PIL import ImageFile
import re
import threading

ImageFile.LOAD_TRUNCATED_IMAGES = True

td_topleft = None
td_high = 0
td_low = 0
enemy_topleft =None

class ImageProcessor:
    def __init__(self):
        self.bms = BmsInterface()
        self.event_start = threading.Event()
        self.event_stop = threading.Event()

    def rec_main(self):
        while True:
            time.sleep(0.1)
            valid = self.getImage("mfdleft")
            if valid:
                enemy_topleft=self.match_enemy()
                # pt_td,wide_td,height_td = self.match_td()
                pt_td=self.match_td()
                if pt_td:
                    # line=self.detect_td_line(pt_td, wide_td, height_td)
                    line = self.detect_td_line(pt_td)
                    if line == 0:
                        if not enemy_topleft:
                            self.move_td()
                            continue
                    else:
                        self.process_td(pt_td)
                lock_toplef=self.match

            # logger.warn("...waiting for start event...")
            # self.event_start.wait()
            # logger.warn("...start an episode...")
            # if self.event_stop.is_set():
            #     logger.warn("...stop an episode...")
            #     self.event_stop.clear()
            #     break





    # def command(self):
    #     self.bms.command_socket.sendto("K:329", self.bms.command_addr)
    #     self.bms.command_socket.sendto("K:264", self.bms.command_addr)

    def getImage(self, msg):
        self.bms.image_socket.send(msg)
        stringData = self.bms.image_socket.recv(1024*1024)
        aa = len(stringData)
        # print aa
        if len(stringData) > 0:
            hex_data=  base64.b64decode(stringData) #base64解码图片
            radar_img = open('imgout.bmp', 'wb')
            radar_img.write(hex_data)
            radar_img.close()
            valid=True
            try:
                #   Image.open('imgout.bmp').verify()
                #   os.system("for i in *.bmp;do convert ${i} ${i%bmp}jpg;done")
                os.system("convert imgout.bmp imgout.jpg")
                print'aaaa'
            except OSError:
                valid =False
                logger.error("convert bmp ")
            # time.sleep(0.5)
        return valid



    def match_enemy(self,value=0.9):
        global enemy_topleft
        img_rgb = cv2.imread('./imgout.jpg')
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        Target=cv2.imread('./enemy.jpg')
        template = cv2.cvtColor(Target, cv2.COLOR_BGR2GRAY)
        wide, height = template.shape[::-1]
        self.value = value
        threshold = value
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)

        if len(loc[0]) != 0:
            enemy_pt=loc[1][0],loc[0][0]
            print enemy_topleft
            enemy_topleft = (int(enemy_pt[0]),int(enemy_pt[1]))
            return enemy_topleft
        else:
            enemy_topleft=None
            return None


    def match_td(self, value=0.7):
        global td_topleft
        img_rgb = cv2.imread('./imgout.jpg')
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        # Target = cv2.imread('./template/td.jpg')
        Target = cv2.imread('./td.jpg')
        template = cv2.cvtColor(Target, cv2.COLOR_BGR2GRAY)
        wide_td, height_td = template.shape[::-1]
        self.wide_td = wide_td
        self.height_td = height_td
        self.value = value
        threshold = value
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        if len(loc[0]) != 0:
            pt_td=loc[1][0],loc[0][0]
            # cv2.rectangle(img_rgb, pt_td, (pt_td[0] + wide_td, pt_td[1] + height_td), (7, 249, 151), 2)
            # cv2.imshow('pt_td',img_rgb)
            # cv2.waitKey(0)
            print pt_td
            td_topleft = (int(pt_td[0]),int(pt_td[1]))

            return pt_td
        else:
            pt_td = None
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
            if ((pt_td[0] + self.wide_td < x1 < pt_td[0] + self.wide_td + 40) and (
                        pt_td[1] - 4 < y1 < pt_td[1] + self.height_td + 24) or (
                               pt_td[0] + self.wide_td < x2 < pt_td[0] + self.wide_td + 40) and (pt_td[1] - 4 < y2 < pt_td[1] + self.height_td  + 24)):

                return 0
            else:
                continue


    def move_td(self):
        self.bms.command_socket.sendto("K:101", self.bms.command_addr)
        # self.bms.command_socket.sendto("K:103", self.bms.command_addr)
        logger.debug('command_up: %s' % ('K:101'))
        # if 0 < pt_td[0] < 255 and 0 < pt_td[1] < 255:
        #     self.bms.command_socket.sendto("K:102", self.bms.command_addr)
        #     self.bms.command_socket.sendto("K:104", self.bms.command_addr)
        #     logger.debug('command_down: %s,command_right: %s' % ('K:102', 'K:104'))
        # elif 225 < pt_td[0] + 30 < 450 and 0 < pt_td[1] < 255:
        #     self.bms.command_socket.sendto("K:102", self.bms.command_addr)
        #     self.bms.command_socket.sendto("K:103", self.bms.command_addr)
        #     logger.debug('command_down: %s,command_left: %s' % ('K:102', 'K:103'))
        # elif 0 < pt_td[0] < 225 and 225 < pt_td[1] + 30 < 450:
        #     self.bms.command_socket.sendto("K:101", self.bms.command_addr)
        #     self.bms.command_socket.sendto("K:104", self.bms.command_addr)
        #     logger.debug('command_up: %s,command_right: %s' % ('K:101', 'K:104'))
        # else:
        #
        #     self.bms.command_socket.sendto("K:101", self.bms.command_addr)
        #     self.bms.command_socket.sendto("K:103", self.bms.command_addr)
        #     logger.debug('command_up: %s,command_left: %s' % ('K:101','K:103'))


    def process_td(self, pt_td):
        global td_topleft, td_high, td_low
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
        high = pytesseract.image_to_string(region1, config='--psm 7 -c tessedit_char_whitelist=-0123456789 -c matcher_perfect_threshold=0.98')
        low = pytesseract.image_to_string(region2, config='--psm 7 -c tessedit_char_whitelist=-0123456789 -c matcher_perfect_threshold=0.98')
        logger.debug("high: %s, low: %s" % (high, low))

        # td_topleft, td_high, td_low = (int(pt_td[0]), int(pt_td[1])), int(high), int(low)
        # logger.debug('self.td_topleft: %s, self.td_high:%s, self.td_low:%s' % (self.td_topleft, self.td_high, self.td_low))
        # print(" low: %s" % (low))
        # region1.show()
        # region2.show()
        # region1.save("high.jpg")
        # region2.save("low.jpg")

        matched_high = re.match('^[-]?\d{2}$', high)
        matched_low = re.match('^[-]?\d{2}$', low )
        if matched_high:
            td_high = int(high)
        else:
            logger.warn('match high fail')
            return False

        if matched_low:
            td_low = int(low)
        else:
            logger.warn('match low fail')
            return False

        # logger.debug('td_high: %d, td_low: %d' % (td_high, td_low))
        # print type(pt_td)
        # logger.debug('td_topleft: %s' % (pt_td))


        # logger.debug('td_topleft: %d' % (td_topleft))




   def lock(self):
       return lock_topleft


    def start(self):
        logger.info("set event start...")
        self.event_start.set()

    def stop(self):
        self.event_stop.set()
        logger.info("set event stop...")