from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework import mixins   #mixin
from rest_framework import generics   #mixin
from medical_resources.models import *
from medical_resources.serializers import *
from rest_framework.decorators import api_view
from django.http import HttpResponse
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from django.utils.decorators import method_decorator


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


#搜索
class SearchResultViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        keyword = self.request.query_params.get("keyword", "")
        return SupAndDem.objects.filter(Q(goods__contains=keyword)  )
    serializer_class = SupAndDemSerializer









    # class MedicalSuppliesTypeViewSet(viewsets.ModelViewSet):
    #     queryset = MedicalSuppliesType.objects.all()
    #     serializer_class = MedicalSuppliesTypeSerializer

    # class MedicalSuppliesViewSet(viewsets.ModelViewSet):
    #     queryset = MedicalSupplies.objects.all()
    #     serializer_class = MedicalSuppliesSerializer