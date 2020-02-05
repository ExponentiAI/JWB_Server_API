#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time    : 2020/1/30 1:44 下午 
# @Author  : Roger 
# @Version : V 0.1
# @Email   : 550997728@qq.com
# @File    : serializers.py.py

from django.contrib.auth.models import User, Group
from rest_framework import serializers
from medical_resources.models import *
from rest_framework.request import Request


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class UserInfoSerializer(serializers.HyperlinkedModelSerializer):  # user序列化器
    class Meta:
        model = UserInfo
        fields = '__all__'


class DemandSerializer(serializers.ModelSerializer):  # 供求序列化器
    u_id = UserInfoSerializer()

    class Meta:
        model = Demand
        fields = '__all__'


class MaterialSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'


class DemandDataSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField(source='Material.count', read_only=True)

    class Meta:
        model = Demand
        fields = ('u_id', 'm_id', 'count', 's_lon', 's_lat', 's_nation', 's_city', 's_province', \
                  's_street', 's_street_number', 's_content', 's_type', \
                  's_range', 's_aging', 's_subtime')


class MaterialDataSerializer(serializers.ModelSerializer):
    # 首页展示serializer
    class Meta:
        model = Material
        fields = ('m_id', 'type', 'count', 'goods_name')
