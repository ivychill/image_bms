#!/usr/bin/env python
# encoding: utf-8
'''

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
class HUD_ImageProcessor:
    def __init__(self):
        self.bms = BmsInterface()
        self.event_start = threading.Event()
        self.event_stop = threading.Event()

    def HUD_rec_main(self):
        while True:
            time.sleep(0.1)
            self.getImage_HUD("hud")


    def getImage_HUD(self, msg_HUD):
        self.bms.image_socket.send(msg_HUD)
        stringData_HUD = self.bms.image_socket.recv(1024 * 1024)
        aa = len(stringData_HUD)
        # print aa
        if len(stringData_HUD) > 0:
            hex_data = base64.b64decode(stringData_HUD)  # base64解码图片
            radar_img = open('imgout_HUD.bmp', 'wb')
            radar_img.write(hex_data)
            radar_img.close()
            valid_HUD = True
            try:
                os.system("convert imgout_HUD.bmp imgout_HUD.jpg")
            except OSError:
                valid_HUD = False
                logger.error("convert bmp ")
            # time.sleep(0.5)
        return valid_HUD
