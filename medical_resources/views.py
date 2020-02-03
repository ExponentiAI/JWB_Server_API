from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from medical_resources.serializers import *
from django.http import HttpResponse
from django.db.models import Q


class UserViewSet(viewsets.ModelViewSet):
    """
    允许用户查看或编辑的API路径。
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    允许组查看或编辑的API路径。
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class JSONResponse(HttpResponse):
    """
    用于返回JSON数据.
    """

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


class UserInfoViewSet(viewsets.ModelViewSet):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer


class SupAndDemViewSet(viewsets.ModelViewSet):
    queryset = SupAndDem.objects.all()
    serializer_class = SupAndDemSerializer


class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer


# 搜索
class SearchResultViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        keyword = self.request.query_params.get("keyword", "")
        return SupAndDem.objects.filter(Q(goods__contains=keyword))
    serializer_class = SupAndDemSerializer
