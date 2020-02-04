from django.shortcuts import render

from rest_framework import viewsets
from medical_resources.serializers import *
from django.http import HttpResponse
from django.db.models import Q
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
import math
from django.http import HttpResponse
from django.http import JsonResponse

from medical_resources.utils import get_lat_lon_range


class JSONResponse(HttpResponse):
    """
    用于返回JSON数据.
    """

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


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


# 纬度1度是111KM,1分是1.85KM
@csrf_exempt
def get_hot_info(request):
    if request.method == 'POST':
        # 解析post数据
        data = JSONParser().parse(request)
        longitude = float(data['longitude'])
        latitude = float(data['latitude'])
        km = float(data['km'])
        items_count = int(data['items_count'])
        max_lat, max_lot, min_lat, min_lot = get_lat_lon_range(latitude, longitude, km)
        # id__gte=724 >=724  ; id__lte=724 <=724
        queryset = SupAndDem.objects.filter(lat__lte=max_lat, lot__lte=max_lot,
                                            lat__gte=min_lat, lot__gte=min_lot).order_by('time')[:items_count]
        serializer = SupAndDemModelSerializer(queryset, many=True)
        return JSONResponse(serializer.data)


@csrf_exempt
def get_new_info(request):
    if request.method == 'POST':
        # 解析post数据
        data = JSONParser().parse(request)
        longitude = float(data['longitude'])
        latitude = float(data['latitude'])
        km = float(data['km'])
        items_count = int(data['items_count'])
        max_lat, max_lot, min_lat, min_lot = get_lat_lon_range(latitude, longitude, km)
        # id__gte=724 >=724  ; id__lte=724 <=724
        queryset = SupAndDem.objects.filter(lat__lte=max_lat, lot__lte=max_lot,
                                            lat__gte=min_lat, lot__gte=min_lot).order_by('time')[:items_count]
        serializer = SupAndDemModelSerializer(queryset, many=True)
        return JSONResponse(serializer.data)
    else:
        pass


@csrf_exempt
def get_me_info(request):
    if request.method == 'POST':
        # 解析post数据
        data = JSONParser().parse(request)
        u_id = str(data['u_id'])
        items_count = int(data['items_count'])
        queryset = SupAndDem.objects.filter(u_id=u_id).order_by('time')[:items_count]
        serializer = SupAndDemModelSerializer(queryset, many=True)
        return JSONResponse(serializer.data)
    else:
        pass
