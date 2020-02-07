from django.shortcuts import render
from django.core.paginator import Paginator
import json
from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer

from medical_resources.fuck_django import demand2json
from medical_resources.serializers import *
from django.http import HttpResponse
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from medical_resources.models import *
from django.views.decorators.csrf import csrf_exempt

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
import math
from django.http import HttpResponse
from django.http import JsonResponse

from medical_resources.utils import get_lat_lon_range
import requests

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


# 用户登录
def UserLogin(request):
    if request.method == 'POST':

        # str = '{"appid":111,"secret":1,"js_code":"sss","grant_type":66.66}'
        loginCodeData = JSONParser().parse(request)
        appid = loginCodeData['appid']
        secret = loginCodeData['secret']
        js_code = loginCodeData['js_code']
        grant_type = loginCodeData['grant_type']

        #GET https://api.weixin.qq.com/sns/jscode2session?appid=APPID&secret=SECRET&js_code=JSCODE&grant_type=authorization_code
        getUserSesstionDataURL =  "https://api.weixin.qq.com/sns/jscode2session?appid=" + appid \
                                  + "&secret=" + secret + "&js_code=" + js_code \
                                  + "&grant_type=" + grant_type
        resp = requests.get(getUserSesstionDataURL)
        userSesstionData = json.loads(resp.text)
        # userSesstionData = JSONParser().parse(resp.text)
        return JsonResponse(userSesstionData)

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


# 提交供应和需求信息
@csrf_exempt
def SupAndDem(request):
    print('if外层')
    if request.method == 'POST':
        print('if内层')
        afferent_data = request.POST
        print('开始存储')
        print(afferent_data['u_id'])
        print(request.POST)
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
        print('demand存储结束')
        goods_arr = ast.literal_eval(afferent_data['goods'])
        print(afferent_data['goods'])
        print(type(goods_arr))
        print('开始for')
        for index, value in enumerate(goods_arr):
            print(index, value, )
            Material.objects.create(
                m_id=demand,
                type=index,
                goods_name=goods_arr[index]['goods_name'],
                count=goods_arr[index]['num_or_price']
            )
        return JsonResponse({"msg": "操作成功！"}, status=status.HTTP_201_CREATED)

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
def get_new_info(request, pindex):
    if request.method == 'POST':
        if pindex == "":  # django中默认返回空值，所以加以判断，并设置默认值为1
            pindex = 1
        else:  # 如果有返回在值，把返回值转为整数型
            pindex = int(pindex)

        # 解析post数据
        data = JSONParser().parse(request)
        longitude = float(data['longitude'])
        latitude = float(data['latitude'])
        km = float(data['search_range'])
        page_items_count = int(data['page_items_count'])
        max_lat, max_lot, min_lat, min_lot = get_lat_lon_range(latitude, longitude, km)

        # id__gte=724 >=724  ; id__lte=724 <=724
        queryset = Demand.objects.filter(s_lat__lte=max_lat, s_lon__lte=max_lot,
                                         s_lat__gte=min_lat, s_lon__gte=min_lot).order_by('s_subtime')
        paginator = Paginator(queryset, page_items_count)  # 实例化Paginator, 每页显示page_items_count条数据

        page = paginator.page(1) if pindex > int(paginator.num_pages) else paginator.page(pindex)

        """
        [OrderedDict([('m_id', 5), ('type', 0), ('count', 100), ('goods_name', '口罩')]),
         OrderedDict([('m_id', 5), ('type', 1), ('count', 100), ('goods_name', '口罩')])]
        """
        return JSONResponse(demand2json(page))
    else:
        pass


@csrf_exempt
def res_details(request):
    if request.method == 'POST':
        # 解析post数据
        data = JSONParser().parse(request)
        m_id = str(data['m_id'])
        queryset = Material.objects.filter(m_id=m_id).order_by('type')
        serializer = MaterialDataSerializer(queryset, many=True)
        return JSONResponse(serializer.data)
    else:
        pass


@csrf_exempt
def get_me_info(request, pindex):
    if request.method == 'POST':

        if pindex == "":  # django中默认返回空值，所以加以判断，并设置默认值为1
            pindex = 1
        else:  # 如果有返回在值，把返回值转为整数型
            pindex = int(pindex)

        # 解析post数据
        data = JSONParser().parse(request)
        u_id = str(data['u_id'])
        page_items_count = int(data['page_items_count'])

        queryset = Demand.objects.filter(u_id=u_id).order_by('s_subtime')

        paginator = Paginator(queryset, page_items_count)  # 实例化Paginator, 每页显示page_items_count条数据

        page = paginator.page(1) if pindex > int(paginator.num_pages) else paginator.page(pindex)

        return JSONResponse(demand2json(page))
    else:
        pass


@csrf_exempt
def store_list(request, pindex):
    """
    search based on keyword on table demand. return demand and user infor.
    """
    if request.method == 'GET':
        if pindex == "":  # django中默认返回空值，所以加以判断，并设置默认值为1
            pindex = 1
        else:  # 如果有返回在值，把返回值转为整数型
            pindex = int(pindex)
        keyword = request.GET.get('keyword')
        page_items_count = request.GET.get('page_items_count')

        queryset = Demand.objects.filter(store_name__icontains=keyword)
        paginator = Paginator(queryset, page_items_count)  # 实例化Paginator, 每页显示page_items_count条数据

        page = paginator.page(1) if int(pindex) > int(paginator.num_pages) else paginator.page(pindex)

        serializer = DemandJoinSerializer(page, many=True)
        return JSONResponse(serializer.data)
    else:
        pass
