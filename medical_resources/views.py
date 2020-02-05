from django.shortcuts import render
import json
from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from medical_resources.serializers import *
from django.http import HttpResponse
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from medical_resources.models import *

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


class UserInfoViewSet(viewsets.ModelViewSet):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer


import ast


# 提交供应和需求信息
def SupAndDem(request):
    if request.method == 'POST':
        afferent_data = request.POST
        demand = Demand.objects.create(
            u_id=UserInfo.objects.get(open_id=afferent_data['u_id']),
            s_lon=afferent_data['lon'],
            s_lat=afferent_data['lat'],
            s_nation=afferent_data['nation'],
            s_city=afferent_data['city'],
            s_province=afferent_data['province'],
            s_district=afferent_data['district'],
            s_street=afferent_data['street'],
            s_street_number=afferent_data['street_number'],
            s_content=afferent_data['content'],
            s_type=afferent_data['type'],
            s_range=afferent_data['range'],
            s_aging=afferent_data['aging'],
            s_subtime=afferent_data['subtime']
        )

        goods_arr = ast.literal_eval(afferent_data['goods'])
        for i in goods_arr:
            Material.objects.create(
                m_id=demand,
                type=i,
                goods_name=goods_arr[i]['goods_name'],
                count=goods_arr[i]['num_or_price']
            )
        return JsonResponse({"msg": "操作成功！"}, status=status.HTTP_201_CREATED)

        # if demand_exists:
        #     return JsonResponse({"msg": "操作成功！"})
        # else:
        #     return JsonResponse({"msg":"操作失败！"})


# 搜索
# class SearchResultViewSet(viewsets.ModelViewSet):
#     def get_queryset(self):
#         keyword = self.request.query_params.get("keyword", "")
#         print('keyword')
#         return SupAndDem.objects.filter(Q(content__contains=keyword))
#     serializer_class = SupAndDemSerializer


# UserInfo.objects.create(
#          open_id = 1,
#          u_type = 1,
#          nick_name = 'sds',
#          avatar_url='sssss',
#          gender='sds',
#          store_name='sds',
#          m_longitude=123213,
#          m_latitude=45454,
#          nation='sds',
#          city='sds',
#          province='sds',
#          district='sds',
#          street='sds',
#          street_number='sds'
#
#      )

# 纬度1度是111KM,1分是1.85KM

@csrf_exempt
def get_new_info(request):
    if request.method == 'POST':
        # 解析post数据
        data = JSONParser().parse(request)
        longitude = float(data['longitude'])
        latitude = float(data['latitude'])
        km = float(data['km'])
        items_count = int(data['count'])
        max_lat, max_lot, min_lat, min_lot = get_lat_lon_range(latitude, longitude, km)
        # id__gte=724 >=724  ; id__lte=724 <=724
        queryset = Demand.objects.filter(s_lat__lte=max_lat, s_lon__lte=max_lot,
                                         s_lat__gte=min_lat, s_lon__gte=min_lot).order_by('s_subtime')[:items_count]
        serializer = DemandDataSerializer(queryset, many=True)
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
        queryset = Demand.objects.filter(u_id=u_id).order_by('time')[:items_count]
        serializer = DemandSerializer(queryset, many=True)
        return JSONResponse(serializer.data)
    else:
        pass
