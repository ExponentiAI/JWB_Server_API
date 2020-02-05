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
from django.views.decorators.csrf import csrf_exempt
class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

class UserInfoViewSet(viewsets.ModelViewSet):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer


import ast
#提交供应和需求信息
@csrf_exempt
def SupAndDem(request):
    print('if外层')
    if  request.method == 'POST':
        print('if内层')
        afferent_data = request.POST
        print('开始存储')
        print(afferent_data['u_id'])
        print(request.POST)
        demand = Demand.objects.create(
            u_id=UserInfo.objects.get(open_id = afferent_data['u_id']),
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
        print('demand存储结束')
        goods_arr = ast.literal_eval(afferent_data['goods'])
        print(afferent_data['goods'])
        print(type(goods_arr))
        print('开始for')
        for index,value in enumerate(goods_arr):
            print(index,value,)
            Material.objects.create(
                m_id = demand,
                type = index,
                goods_name = goods_arr[index]['goods_name'],
                count = goods_arr[index]['num_or_price']
            )
        return JsonResponse({"msg": "操作成功！"},status=status.HTTP_201_CREATED)



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