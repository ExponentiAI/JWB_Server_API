#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time    : 2020/1/30 4:22 下午
# @Author  : Roger
# @Version : V 0.1
# @Email   : 550997728@qq.com
# @File    : serializers.py.py

from django.db import models


class MedicalSuppliesType(models.Model):
    t_id = models.AutoField(primary_key=True, verbose_name='物资类型ID', unique=True)
    t_name = models.CharField(max_length=15, verbose_name='物资类型', unique=True)

    def __str__(self):
        return self.t_name


class UserInfo(models.Model):
    def __str__(self):
        return self.nick_name

    u_id = models.AutoField(primary_key=True, verbose_name='用户openID')
    nick_name = models.CharField(max_length=15, verbose_name='用户名')
    avatar_url = models.CharField(max_length=20, verbose_name='头像')
    gender = models.CharField(max_length=20, verbose_name='性别')


class MedicalSupplies(models.Model):
    class Meta:
        verbose_name = 'MedicalSupplies Data'
        verbose_name_plural = 'MedicalSupplies Data'

    m_id = models.AutoField(primary_key=True, verbose_name='物资ID', unique=True)
    u_id = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name='用户openID')
    m_name = models.CharField(max_length=15, verbose_name='物品名称')
    m_type = models.ForeignKey('MedicalSuppliesType', to_field='t_name', on_delete=models.CASCADE,
                               verbose_name='物资类型')
    m_store_name = models.CharField(max_length=15, verbose_name='商店名')
    m_longitude = models.DecimalField(max_digits=40, decimal_places=30, verbose_name='经度')
    m_latitude = models.DecimalField(max_digits=40, decimal_places=30, verbose_name='纬度')
    m_price = models.DecimalField(max_digits=10, decimal_places=4, verbose_name='价格', default=0)
    m_count = models.DecimalField(max_digits=20, decimal_places=4, verbose_name='数量', default=0)
    m_prescription = models.IntegerField(verbose_name='发布时效')
    m_describe = models.CharField(max_length=200, verbose_name='描述')
    m_range = models.IntegerField(verbose_name='位置范围')
    m_address = models.CharField(max_length=100, verbose_name='地址')
    m_city = models.CharField(max_length=100, verbose_name='城市')
    m_time = models.DateTimeField(max_length=20, verbose_name='时间')
