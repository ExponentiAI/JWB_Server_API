#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time    : 2020/2/7 3:57 下午 
# @Author  : Roger 
# @Version : V 0.1
# @Email   : 550997728@qq.com
# @File    : fuck_django.py

def demand2json(queryset):
    """
    """
    datas = []
    for item in queryset:
        data = {}
        # 头像
        data['avatar_url'] = item.u_id.avatar_url
        # 商店名
        data['store_name'] = item.store_name
        # 经度
        data['s_lon'] = item.s_lon
        # 纬度
        data['s_lat'] = item.s_lat
        # 国家
        data['s_nation'] = item.s_nation
        # 城市
        data['s_city'] = item.s_city
        # 省份
        data['s_province'] = item.s_province
        # 街道
        data['s_street'] = item.s_street
        # 街号
        data['s_street_number'] = item.s_street_number
        # 内容
        data['s_content'] = item.s_content
        # 类型
        data['s_type'] = item.s_type
        # 范围
        data['s_range'] = item.s_range
        # 时效
        data['s_aging'] = item.s_aging
        # 时间
        data['s_subtime'] = item.s_subtime
        # material
        data['details_info'] = material2json(item.m_id.all())
        datas.append(data)
    return datas


def material2json(queryset):
    """
    ('m_id', 'type', 'count', 'goods_name')
    """
    datas = []
    for item in queryset:
        data = {}
        # 类型
        data['type'] = item.type
        # 数量
        data['count'] = item.count
        # 商店名
        data['goods_name'] = item.goods_name
        datas.append(data)
    return datas
