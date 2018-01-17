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
import time
import socket

from SimpleXMLRPCServer import SimpleXMLRPCServer

#from bitmap import BitMap
import os
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

global s #全局

def connectServer(ip,port):
    global s
    address = (ip,port)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(address)
        return 1
    except Exception, e:
        return 0
# end connectServer

def getImage(msg):
    global s
    while True:
        s.send(msg)
        stringData = s.recv(1024*1024)

        if len(stringData) > 0:
            hex_data=  base64.b64decode(stringData) #base64解码图片
            leidaimg = open('imgout.bmp', 'wb')
            leidaimg.write(hex_data)
            leidaimg.close()
            os.system("for i in *.bmp;do convert ${i} ${i%bmp}jpg;done")
            # img_cv = cv2.imread("imgout.jpg")
            # cv2.imshow('image', img_cv)
            # cv2.waitKey(1)

            def match_img(image_path, Target, value):
                #image = Image.open(image_path)
            #
            #     # size = ()
            #     # for element in image.size:
            #     #     # print element, type(element)
            #     #     size += (element * 4,)
            #     # scaled_image = image.resize(size, Image.ANTIALIAS)
            #     # scaled_image.save("scaled_img.png")
            #
                img_rgb = cv2.imread(image_path)
                img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
                template = cv2.imread(Target, 0)
                w, h = template.shape[::-1]
                threshold = value
                res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
                loc = np.where(res >= threshold)
                for pt in zip(*loc[::-1]):
                    cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (7, 249, 151), 2)
                cv2.rectangle(img_rgb, (pt[0] + w, pt[1]-12), (pt[0] + w + 40, pt[1] + 8), (7, 249, 151), 2)
                cv2.rectangle(img_rgb, (pt[0] + w, pt[1] + h-5), (pt[0] + w + 40, pt[1] + h + 15), (7, 249, 151), 2)
                cv2.imshow('Detected', img_rgb)

                cv2.waitKey(10)

                image = Image.open(image_path)
                #print image.format, image.size, image.mode

                box1 = (pt[0] + w, pt[1] -12, pt[0] + w + 40, pt[1] + 8)
                box2 = (pt[0] + w, pt[1] + h-5,pt[0] + w + 40, pt[1] + h + 15)
                region1 = image.crop(box1)
                region2 = image.crop(box2)
                high = pytesseract.image_to_string(region1, config='--psm 7 -c tessedit_char_whitelist=-0123456789')
                low = pytesseract.image_to_string(region2, config='--psm 7 -c tessedit_char_whitelist=-0123456789')
                print("high: %s, low: %s" % (high, low))
                region1.show()
                region2.show()
                region1.save("high.jpg")
                region2.save("low.jpg")




            image = ('imgout.jpg')
            Target = ('tt.jpg')
            value = 0.8
            match_img(image, Target, value)

            print 'the data received is'
            time.sleep(0.5)
            continue
        else:
            break

    s.close()

#end getImage
def match_img(image)
    return img_rgb,pt

def recongize_image_high_and_low(image)
    return high, low

#
def recognize_
    return

# return: True/False
def detect_line(image):
    return False


def detect_wall(image):
    return False

def register_rpc():
    server = SimpleXMLRPCServer(("192.168.24.108", 5001), allow_none=True)  # 确定URL和端口
    server.register_function(get_td, "get_td")  # 注册is_even函数
    server.serve_forever()  # 启动服务器,并使其对这个连接可用

def get_td():

    # return topleft, high, low

if __name__ == "__main__":

    connectServer('192.168.20.114', 13000)
    getImage("mfdleft")
    register_rpc()
    # time.sleep(300000)