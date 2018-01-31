#!/usr/bin/env python
# encoding: utf-8


from SimpleXMLRPCServer import SimpleXMLRPCServer
import image_processor
import time
from log_config import *

image_proc = None

def register_rpc(image_processor):
    global image_proc
    image_proc = image_processor
    # server = SimpleXMLRPCServer(("192.168.24.108", 5001), allow_none=True)
    server = SimpleXMLRPCServer(("192.168.20.129", 5001), allow_none=True)
    server.register_function(get_td, "get_td")  # 注册is_even函数
    server.register_function(get_td_high_low, "get_td_high_low")
    server.register_function(get_enemy_coord, "get_enemy_coord")
    server.register_function(get_Index, "get_Index")
    server.register_function(get_Ropt, "get_Ropt")
    server.register_function(get_Rpi, "get_Rpi")
    server.register_function(get_Rtr, "get_Rtr")
    server.register_function(get_miss_clock, "get_miss_clock")
    server.register_function(start, "start")
    server.register_function(stop, "stop")
    server.register_function(reboot, "reboot")
    server.serve_forever()  # 启动服务器,并使其对这个连接可用

def get_td():
    # logger.debug("td_topleft: %s" % (image_processor.td_topleft))
    return image_processor.td_topleft

def get_td_high_low():
    logger.debug("td_high: %s, td_low: %s" % (image_processor.td_high, image_processor.td_low))
    return image_processor.td_high, image_processor.td_low

def get_enemy_coord():
    # print type(image_processor.enemy_topleft[0])
    print image_processor.enemy_topleft
    # logger.debug("enemy_topleft: %s" % (image_processor.enemy_topleft))
    return image_processor.enemy_topleft

def get_Index():
    print  image_processor.Index_topleft
    return image_processor.Index_topleft

def get_Ropt():
    print image_processor.Ropt_topleft
    return image_processor.Ropt_topleft

def get_Rpi():
    print image_processor.Rpi_topleft
    return image_processor.Rpi_topleft

def get_Rtr():
    print image_processor.Rtr_topleft
    return image_processor.Rtr_topleft

def get_miss_clock():
    print image_processor.miss_clock_digit,image_processor.fcr_nose_up
    return image_processor.miss_clock_digit,image_processor.fcr_nose_up

def start():
    image_proc.start()

def stop():
    image_proc.stop()

def reboot():
    image_proc.reboot()