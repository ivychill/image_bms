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
from random import *

ImageFile.LOAD_TRUNCATED_IMAGES = True

td_topleft = None
td_high = None
td_low = None
enemy_topleft = None

lock_topleft=None
Index_topleft=None
Ropt_topleft=None
Rpi_topleft=None
Rtr_topleft=None
miss_clock_digit = None
fcr_nose_up = None
class ImageProcessor:
    def __init__(self):
        self.bms = BmsInterface()
        self.event_start = threading.Event()
        self.event_stop = threading.Event()

    def ai_main(self):
        while True:
            logger.warn("...waiting for start event...")
            self.event_start.wait()
            time.sleep(12)
            logger.warn("...start an episode...")
            while True:
                time.sleep(0.1)
                valid_Lmfd = self.getImage_Lmfd("mfdleft")
                if valid_Lmfd:
                    enemy_topleft=self.match_enemy()
                    # pt_td,wide_td,height_td = self.match_td()
                    pt_td=self.match_td()

                    if enemy_topleft is None:
                        if pt_td is not None:
                            line = self.detect_td_line(pt_td)
                            if line == 0:
                                self.move_td()
                                continue
                            else:
                                high,low=self.process_td(pt_td)
                                valid_rec=self.rec_high_low(high,low)
                                if valid_rec:
                                    self.move_td()

                if self.event_stop.is_set():
                    logger.warn("...stop an episode...")
                    self.event_stop.clear()
                    break

    def rec_main(self):
        while True:
            time.sleep(0.1)
            valid_Lmfd = self.getImage_Lmfd("mfdleft")
            if valid_Lmfd:
                enemy_topleft = self.match_enemy()
                pt_td = self.match_td()

                if enemy_topleft is None:
                    if pt_td is not None:
                        line = self.detect_td_line(pt_td)
                        if line == 0:
                            self.move_td()
                            continue
                        else:
                            high, low = self.process_td(pt_td)
                            valid_rec = self.rec_high_low(high, low)
                            if valid_rec:
                                self.move_td()
                                continue

                lock_topleft = self.match_lock()
                if lock_topleft is not None:
                    self.match_Index()
                    self.match_Ropt()
                    self.match_Rpi()
                    self.match_Rtr()

                self.Miss_clock_and_Fcr_rec()


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


    def getImage_Lmfd(self, msg):
        self.bms.image_socket.send(msg)
        stringData_Lmfd = self.bms.image_socket.recv(1024*1024)
        aa = len(stringData_Lmfd)
        # print aa
        if len(stringData_Lmfd) > 0:
            hex_data=  base64.b64decode(stringData_Lmfd) #base64解码图片
            radar_img = open('imgout_Lmfd.bmp', 'wb')
            radar_img.write(hex_data)
            radar_img.close()
            valid_Lmfd=True
            try:
                os.system("convert imgout_Lmfd.bmp imgout_Lmfd.jpg")
            except OSError:
                valid_Lmfd =False
                logger.error("convert bmp ")
            # time.sleep(0.5)
        return valid_Lmfd




    def match_enemy(self,value=0.99):
        global enemy_topleft
        img_rgb = cv2.imread('./imgout_Lmfd.jpg')
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        Target=cv2.imread('./enemy.jpg')
        template = cv2.cvtColor(Target, cv2.COLOR_BGR2GRAY)
        wide, height = template.shape[::-1]
        self.value = value
        threshold = value
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res)
        if maxVal >= threshold:
            enemy_pt = maxLoc
        # loc = np.where(res >= threshold)
        # if len(loc[0]) != 0:
            # enemy_pt=loc[1][0],loc[0][0]
            # enemy_pt = loc[1][-1], loc[0][0]
            print enemy_topleft
            enemy_topleft = (int(enemy_pt[0]),int(enemy_pt[1]))
            return enemy_topleft
        else:
            enemy_topleft=None
            return None


    def match_td(self, value=0.7):
        global td_topleft
        img_rgb = cv2.imread('./imgout_Lmfd.jpg')
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
        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res)
        if maxVal >= threshold:
            pt_td = maxLoc
        # loc = np.where(res >= threshold)
        # if len(loc[0]) != 0:
        #     # pt_td=loc[1][0],loc[0][0]
        #     pt_td = loc[1][-1], loc[0][0]
            # cv2.rectangle(img_rgb, pt_td, (pt_td[0] + wide_td, pt_td[1] + height_td), (7, 249, 151), 2)
            # cv2.imshow('pt_td',img_rgb)
            # cv2.waitKey(0)
            print pt_td
            td_topleft = (int(pt_td[0]),int(pt_td[1]))

            return pt_td
        else:
            td_topleft = None
            return None

    def detect_td_line(self, pt_td):
        img_rgb = cv2.imread('./imgout_Lmfd.jpg')
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
        n = random()
        logger.debug('randge: %s' % (n))
        if 0.0 <= n <=0.25:
            self.bms.command_socket.sendto("K:101", self.bms.command_addr)
            logger.debug('command_up: %s' % ('K:101'))
        elif 0.25 < n <=0.5:
            self.bms.command_socket.sendto("K:102", self.bms.command_addr)
            logger.debug('command_up: %s' % ('K:102'))
        elif 0.5 <n <=0.75:
            self.bms.command_socket.sendto("K:103", self.bms.command_addr)
            logger.debug('command_up: %s' % ('K:103'))
        else:
            self.bms.command_socket.sendto("K:104", self.bms.command_addr)
            logger.debug('command_up: %s' % ('K:104'))
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
        image = Image.open('./imgout_Lmfd.jpg')
        # image = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        # box1 = (pt_td[0] + wide_td, pt_td[1] -4, pt_td[0] + wide_td + 40, pt_td[1] + 19)
        # box2 = (pt_td[0] + wide_td, pt_td[1] + height_td - 1 ,pt_td[0] + wide_td + 40, pt_td[1] + height_td + 24)
        box1 = (pt_td[0] + self.wide_td-2, pt_td[1] -8, pt_td[0] + self.wide_td + 40, pt_td[1] + 15)
        box2 = (pt_td[0] + self.wide_td-2, pt_td[1] + self.height_td-3, pt_td[0] + self.wide_td + 40, pt_td[1] + self.height_td + 24)
        region1 = image.crop(box1)
        region2 = image.crop(box2)
        region1.save("high.jpg")
        region2.save("low.jpg")
        # region1.show()
        # region2.show()

        # matcher_good_threshold      0.125
        # matcher_great_threshold     0
        # matcher_perfect_threshold   0.02
        # matcher_bad_match_pad       0.15
        # high = pytesseract.image_to_string(region1, config='--psm 7 -c tessedit_char_whitelist=-0123456789 -c matcher_perfect_threshold=0.9')
        # low = pytesseract.image_to_string(region2, config='--psm 7 -c tessedit_char_whitelist=-0123456789 -c matcher_perfect_threshold=0.9')
        high = pytesseract.image_to_string(region1, config='--psm 7 -c tessedit_char_whitelist=-0123456789')
        low = pytesseract.image_to_string(region2, config='--psm 7 -c tessedit_char_whitelist=-0123456789')
        logger.debug("high: %s, low: %s" % (high, low))
        region1.save("high.jpg")
        region2.save("low.jpg")
        return high,low

    def rec_high_low(self,high,low):
        global td_high, td_low
        matched_high = re.match('^[-]?\d{2}$', high)
        matched_low = re.match('^[-]?\d{2}$', low)
        if matched_high is not None:
            td_high = int(high)
        else:

            logger.warn('match high fail')
            td_high = None

        if matched_low is not None:
            td_low = int(low)
        else:
            logger.warn('match low fail')
            td_low = None

        if td_high or td_low is None:
            return True
        else:
            return False

        logger.debug('td_high: %d, td_low: %d' % (td_high, td_low))

        if td_high is None or td_low is None:
            return False
        else:
            return True

    def match_lock(self,value=0.99):
        global lock_topleft
        img_rgb = cv2.imread('./imgout_Lmfd.jpg')
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        Target = cv2.imread('./lock_label.jpg')
        template = cv2.cvtColor(Target, cv2.COLOR_BGR2GRAY)
        w, h = template.shape[::-1]
        self.value = value
        threshold = value
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res)
        if maxVal >= threshold:
            pt_lock = maxLoc
        # loc = np.where(res >= threshold)
        # if len(loc[0]) != 0:
        #     pt_lock = loc[1][-1], loc[0][0]
            lock_topleft = (int(pt_lock[0]), int(pt_lock[1]))
            # print lock_topleft
            return lock_topleft
        else:
            lock_topleft = None
            return None


    def match_Index(self,value=0.75):
        global Index_topleft
        img_rgb = cv2.imread('./imgout_Lmfd.jpg')
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        Target = cv2.imread('./Index_label.jpg')
        template = cv2.cvtColor(Target, cv2.COLOR_BGR2GRAY)
        w, h = template.shape[::-1]
        self.value=value
        threshold = value
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res)
        if maxVal >= threshold:
            pt_Index = maxLoc
        # loc = np.where(res >= threshold)
        # if len(loc[0]) != 0:
            # pt_Index=loc[1][0],loc[0][0]
            # pt_Index = loc[1][-1], loc[0][0] + 10
            # loc is topleft corner. mid-point of height should be used.
            # Thus, compensation of 10pix is given to pt_Index.
            Index_topleft= int(pt_Index[1])+10
            # print "Index_topleft is %d" % (Index_topleft)
        else:
            Index_topleft = None


    def match_Ropt(self,value=0.6):
        global Ropt_topleft
        img_rgb = cv2.imread('./imgout_Lmfd.jpg')
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        Target = cv2.imread('./Ropt_label.jpg')
        template = cv2.cvtColor(Target, cv2.COLOR_BGR2GRAY)
        w, h = template.shape[::-1]
        self.value=value
        threshold = value
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res)
        if maxVal >= threshold:
            pt_Ropt = maxLoc
        # loc = np.where(res >= threshold)
        # if len(loc[0]) != 0:
            # pt_Ropt=loc[1][0],loc[0][0]
            # pt_Ropt = loc[1][-1], loc[0][0]
            Ropt_topleft= int(pt_Ropt[1])
            # print "Ropt_topleft is %d" % (Ropt_topleft)
        else:
            Ropt_topleft = None


    def match_Rpi(self,value=0.7):
        global Rpi_topleft
        img_rgb = cv2.imread('./imgout_Lmfd.jpg')
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        Target = cv2.imread('./Rpi_label.jpg')
        template = cv2.cvtColor(Target, cv2.COLOR_BGR2GRAY)
        w, h = template.shape[::-1]
        self.value=value
        threshold = value
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res)
        if maxVal >= threshold:
           pt_Rpi = maxLoc
           if pt_Rpi[1] >220:
        # if len(loc[0]) != 0:
        #     for pt_Rpi in loc[0][:-1]:
        #         if pt_Rpi > 220:
            # pt_Rpi=loc[1][0],loc[0][0]
                    Rpi_topleft= int(pt_Rpi[1])
                    # print 'Rpi_topleft is %d' % (Rpi_topleft)

        else:
            Rpi_topleft= None


    def match_Rtr(self,value=0.85):
        global Rtr_topleft
        img_rgb = cv2.imread('./imgout_Lmfd.jpg')
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        Target = cv2.imread('./Rtr_label.jpg')
        template = cv2.cvtColor(Target, cv2.COLOR_BGR2GRAY)
        w, h = template.shape[::-1]
        self.value=value
        threshold = value
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res)
        if maxVal >= threshold:
            pt_Rtr = maxLoc
        # loc = np.where(res >= threshold)
        # if len(loc[0]) != 0:
            # pt_Rtr=loc[1][0],loc[0][0]
            # pt_Rtr = loc[1][-1], loc[0][0]
            Rtr_topleft=int(pt_Rtr[1])
            # print 'Rtr_topleft is %d' % (Rtr_topleft)
        else:
            Rtr_topleft = None

    def Miss_clock_and_Fcr_rec(self):
        global miss_clock_digit,fcr_nose_up
        pt_miss_clock=(386,362)
        wide_miss_clock=40
        heigh_miss_clock=23
        pt_fcr=(383,124)
        wide_fcr=28
        heigh_fcr=22
        image = Image.open('./imgout_Lmfd.jpg')
        box_miss_clock = (pt_miss_clock[0], pt_miss_clock[1], pt_miss_clock[0] + wide_miss_clock, pt_miss_clock[1] + heigh_miss_clock)
        box_fcr = (pt_fcr[0], pt_fcr[1], pt_fcr[0] + wide_fcr,pt_fcr[1] + heigh_fcr)
        region_miss_clock = image.crop(box_miss_clock)
        region_fcr = image.crop(box_fcr)
        miss_clock_digit = pytesseract.image_to_string(region_miss_clock, config='--psm 7')
        fcr_nose_up = pytesseract.image_to_string(region_fcr, config='--psm 7')
        str_miss_clock_digit=str(miss_clock_digit)
        str_fcr_nose_up=str(fcr_nose_up)

        if  str_miss_clock_digit == ',' or len(str_miss_clock_digit) == 0:
            miss_clock_digit = None
            print 'miss_clock_digit : %s' %(miss_clock_digit)
        else:
            print 'miss_clock_digit :%s' %(miss_clock_digit)

        if str_fcr_nose_up == ',' or len(str_fcr_nose_up) == 0:
            fcr_nose_up = None
            print 'fcr_nose_up: %s' %(fcr_nose_up)

        else:
            print 'fcr_nose_up: %s' %(fcr_nose_up)









    def start(self):
        logger.info("set event start...")
        self.event_start.set()

    def stop(self):
        self.event_stop.set()
        logger.info("set event stop...")