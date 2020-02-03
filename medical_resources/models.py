#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time    : 2020/1/30 4:22 下午
# @Author  : Roger
# @Version : V 0.1
# @Email   : 550997728@qq.com
# @File    : serializers.py.py

from django.db import models


class UserInfo(models.Model):
    u_type = models.IntegerField(verbose_name='用户类别', default=9)  # 0商家  1 用户
    open_id = models.IntegerField(verbose_name='用户openID', default=9)
    nick_name = models.CharField(max_length=15, verbose_name='用户名', default="")
    avatar_url = models.CharField(max_length=20, verbose_name='头像', default="")
    gender = models.CharField(max_length=20, verbose_name='性别', default="")
    store_name = models.CharField(max_length=150, verbose_name='商店名称', default="")
    address = models.CharField(max_length=100, verbose_name='商店位置', default='')
    m_longitude = models.DecimalField(max_digits=40, decimal_places=30, verbose_name='经度', default="")
    m_latitude = models.DecimalField(max_digits=40, decimal_places=30, verbose_name='纬度', default="")
    city = models.CharField(max_length=100, verbose_name='城市', default="")
    province = models.CharField(max_length=100, verbose_name='省份', default="")


class SupAndDem(models.Model):  # 供求表
    user = models.IntegerField(verbose_name='user_id', default=9)
    u_id = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name='用户openID', related_name='u_id',
                             default="")
    lon = models.DecimalField(max_digits=40, decimal_places=30, verbose_name='经度', default="")
    lat = models.DecimalField(max_digits=40, decimal_places=30, verbose_name='纬度', default="")
    address = models.CharField(max_length=100, verbose_name='地址', default='')
    city = models.CharField(max_length=100, verbose_name='城市', default="")
    province = models.CharField(max_length=100, verbose_name='省份', default="")
    content = models.CharField(max_length=300, verbose_name='描述', default="")
    type = models.IntegerField(verbose_name='供需类别', default="")  # 0为需求，1为供应
    range = models.IntegerField(verbose_name='位置范围', default="")
    goods = models.CharField(max_length=1000, verbose_name='物资名称', default="")
    aging = models.IntegerField(verbose_name='发布时效', default="")
    time = models.DateTimeField(max_length=20, verbose_name='时间', default="")


class Material(models.Model):  # 供应物资表
    class Meta:
        verbose_name = 'Material Data'
        verbose_name_plural = 'Material Data'

    store_name = models.CharField(max_length=15, verbose_name='商店名')
    lon = models.DecimalField(max_digits=40, decimal_places=30, verbose_name='经度', default="")
    lat = models.DecimalField(max_digits=40, decimal_places=30, verbose_name='纬度', default="")
    price = models.DecimalField(max_digits=10, decimal_places=4, verbose_name='价格', default=0)
    count = models.DecimalField(max_digits=20, decimal_places=4, verbose_name='数量', default=0)
    address = models.CharField(max_length=100, verbose_name='地址', default="")
    city = models.CharField(max_length=100, verbose_name='城市', default="")
    time = models.DateTimeField(max_length=20, verbose_name='时间', default="")
    province = models.CharField(max_length=100, verbose_name='省份', default="")
    goods_name = models.CharField(max_length=100, verbose_name='物资名称', default="")

    def __str__(self):
        return self.store_name
