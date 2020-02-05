#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time    : 2020/2/4 4:04 下午 
# @Author  : Roger 
# @Version : V 0.1
# @Email   : 550997728@qq.com
# @File    : utils.py


def get_lat_lon_range(lat, lon, km):
    """
    # 纬度1度是111KM,1分是1.85KM
    """
    angle = km / 111
    return lat + angle, lon + angle, lat - angle, lon - angle
