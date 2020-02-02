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


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class UserInfoSerializer(serializers.HyperlinkedModelSerializer):   #user序列化器
    class Meta:
        model = UserInfo
        fields = '__all__'

class SupAndDemSerializer(serializers.ModelSerializer):   #供求序列化器
    u_id =  UserInfoSerializer()
    class Meta:
        model = SupAndDem
        fields = '__all__'

class MaterialSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'







# class MedicalSuppliesTypeSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = MedicalSuppliesType
#         fields = '__all__'
#
# class MedicalSuppliesSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = MedicalSupplies
#         fields = '__all__'
