#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time    : 2020/1/30 4:22 下午
# @Author  : Roger
# @Version : V 0.1
# @Email   : 550997728@qq.com
# @File    : serializers.py.py

from django.db import models


class MedicalSupplies(models.Model):
    class Meta:
        verbose_name = 'MedicalSupplies Data'
        verbose_name_plural = 'MedicalSupplies Data'

    m_id = models.CharField(max_length=100, verbose_name='Devices ID')
    m_name = models.CharField(max_length=15, verbose_name='MedicalSupplies Name')
    m_type = models.CharField(max_length=15, verbose_name='MedicalSupplies Type')
    m_store_name = models.CharField(max_length=15, verbose_name='Store Name')
    m_longitude = models.DecimalField(max_digits=40, decimal_places=30, verbose_name='Longitude')
    m_latitude = models.DecimalField(max_digits=40, decimal_places=30, verbose_name='Latitude')
    m_price = models.DecimalField(max_digits=10, decimal_places=4, verbose_name='price', default=0)
    m_count = models.DecimalField(max_digits=20, decimal_places=4, verbose_name='count', default=0)
    m_address = models.CharField(max_length=100, verbose_name='Address')
    m_city = models.CharField(max_length=100, verbose_name='City')
    m_time = models.DateTimeField(max_length=20, verbose_name='Time')


class UserInfo(models.Model):
    u_id = models.CharField(max_length=100, verbose_name='User ID')
    u_name = models.CharField(max_length=15, verbose_name='User Name')
    u_phone = models.CharField(max_length=20, verbose_name='Phone Number')


class MedicalSuppliesType(models.Model):
    pass
