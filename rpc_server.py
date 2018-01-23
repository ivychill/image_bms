#!/usr/bin/env python
# encoding: utf-8


from SimpleXMLRPCServer import SimpleXMLRPCServer
import image_processor

def register_rpc():
    server = SimpleXMLRPCServer(("192.168.24.108", 5001), allow_none=True)  # 确定URL和端口
    server.register_function(get_td, "get_td")  # 注册is_even函数
    server.register_function(get_enemy_coord, "get_enemy_coord")
    server.serve_forever()  # 启动服务器,并使其对这个连接可用

def get_td():
    td_left,td_high,td_low  = image_processor.td_left,image_processor.td_high,image_processor.td_low

    # td_left=image_processor.td_left

    return td_left,td_high,td_low

def get_enemy_coord():
    enemy_left=image_processor.enemy_pt

    return enemy_left