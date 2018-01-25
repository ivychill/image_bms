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
    server.register_function(get_enemy_coord, "get_enemy_coord")
    server.register_function(start, "start")
    server.register_function(stop, "stop")
    server.serve_forever()  # 启动服务器,并使其对这个连接可用

def get_td():
    logger.debug("td_topleft: %s, td_high: %s, td_low: %s" % (image_processor.td_topleft, image_processor.td_high, image_processor.td_low))
    return image_processor.td_topleft, image_processor.td_high, image_processor.td_low

def get_enemy_coord():
    # print type(image_processor.enemy_topleft[0])
    print image_processor.enemy_topleft

    # logger.debug("enemy_topleft: %s" % (image_processor.enemy_topleft))
    return image_processor.enemy_topleft

def start():
    logger.info("started...")
    image_proc.start()

def stop():
    image_proc.stop()

