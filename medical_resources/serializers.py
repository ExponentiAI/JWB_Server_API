#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time    : 2020/1/30 1:44 下午 
# @Author  : Roger 
# @Version : V 0.1
# @Email   : 550997728@qq.com
# @File    : serializers.py.py

from django.contrib.auth.models import User, Group
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


