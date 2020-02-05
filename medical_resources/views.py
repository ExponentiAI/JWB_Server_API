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
class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

class UserInfoViewSet(viewsets.ModelViewSet):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer

#用户注册
def UserRegister(request):
    if request.method == 'POST':
        allData = json.loads(str(request.body,'utf-8'))

        # userInfo, created = UserInfo.objects.get_or_create(open_id=111)
        # if created == False:    #没创建新对象，表示该已注册过
        #     print("oldRegis--%s" % userInfo)
        #     return JsonResponse({"msg": "UserRegistered"}, status=status.HTTP_201_CREATED)
        # elif created == True:
        #     UserInfo.objects.filter(open_id=allData['open_id']).update(**allData)
        #     print("newRegis--%s" % userInfo)
        #     return JsonResponse({"msg": "NewUserRegisterSuccess！"}, status=status.HTTP_201_CREATED)

        try:     #已注册
            userInfo = UserInfo.objects.get(open_id = allData['open_id'])
            print("oldRegis--%s" % userInfo)
            return JsonResponse({"msg": "UserRegistered"},status=status.HTTP_201_CREATED)
        except UserInfo.DoesNotExist:    #未注册
                UserInfo.objects.create (
                u_type = allData['u_type'],
                open_id=allData['open_id'],
                nick_name=allData['nick_name'],
                avatar_url=allData['avatar_url'],
                gender=allData['gender'],
                store_name=allData['store_name'],
                m_longitude=allData['m_longitude'],
                m_latitude=allData['m_latitude'],
                nation=allData['nation'],
                city=allData['city'],
                province=allData['province'],
                district=allData['district'],
                street=allData['street'],
                street_number=allData['street_number']
            )
        print('NewUserRegisterSuccess')
        return JsonResponse({"msg": "NewUserRegisterSuccess"}, status=status.HTTP_201_CREATED)
import ast
#提交供应和需求信息
def SupAndDem(request):
    if  request.method == 'POST':
        afferent_data = request.POST
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

        goods_arr = ast.literal_eval(afferent_data['goods'])
        for i in goods_arr:
            Material.objects.create(
                m_id = demand,
                type = i,
                goods_name = goods_arr[i]['goods_name'],
                count = goods_arr[i]['num_or_price']
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