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
import requests
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
import math
from django.http import HttpResponse
from django.http import JsonResponse

from medical_resources.utils import get_lat_lon_range
import requests
from datetime import datetime


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


class DemandViewSet(viewsets.ModelViewSet):
    queryset = UserInfo.objects.all()
    serializer_class = DemandSerializer


class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

#检查tocken过期
from django.utils import timezone
def check_tocken():
    appinfo = AppInfo.objects.get(appid="wxb038b5f6187b1412")
    appid = appinfo.appid
    secret = appinfo.secret
    subtime = appinfo.subtime
    access_token = appinfo.access_token
    now_time = timezone.now()
    durn = (now_time - subtime).seconds
    print(durn)
    if durn>4000:
        r = requests.get('https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=' + appid + '&secret=' + secret + '')
        appinfo.access_token =  access_token=json.loads(r.text)['access_token']
        appinfo.save()
        print(json.loads(r.text)['access_token'])
        return {'appid':appid,'secret':secret, 'access_token': json.loads(r.text)['access_token']}
    else:
        return {'appid': appid, 'secret': secret, 'access_token': access_token}

# 用户登录
def UserLogin(request):
    if request.method == 'GET':
        app_data = check_tocken()
        appid = app_data['appid']
        secret = app_data['secret']
        js_code = request.GET['js_code']
        grant_type = 'authorization_code'
        resp = requests.get(
            "https://api.weixin.qq.com/sns/jscode2session?appid=" + appid + "&secret=" + secret + "&js_code=" + js_code + "&grant_type=" + grant_type)
        userSesstionData = json.loads(resp.text)
        # userSesstionData = JSONParser().parse(resp.text)
        return JsonResponse(userSesstionData)


# 用户注册
def UserRegister(request):
    if request.method == 'POST':
        allData = json.loads(str(request.body, 'utf-8'))
        # userInfo, created = UserInfo.objects.get_or_create(open_id=111)
        # if created == False:    #没创建新对象，表示该已注册过
        #     print("oldRegis--%s" % userInfo)
        #     return JsonResponse({"msg": "UserRegistered"}, status=status.HTTP_201_CREATED)
        # elif created == True:
        #     UserInfo.objects.filter(open_id=allData['open_id']).update(**allData)
        #     print("newRegis--%s" % userInfo)
        #     return JsonResponse({"msg": "NewUserRegisterSuccess！"}, status=status.HTTP_201_CREATED)
        try:  # 已注册
            userInfo = UserInfo.objects.get(open_id=allData['open_id'])
            print("oldRegis--%s" % userInfo)
            return JsonResponse({"msg": "UserRegistered"}, status=status.HTTP_201_CREATED)
        except UserInfo.DoesNotExist:  # 未注册
            UserInfo.objects.create(
                u_type=allData['u_type'],
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


import time


import ast
import urllib.parse
import urllib.request
import json
import argparse

from urllib.parse import urlencode

# 提交供应和需求信息
# 检查敏感词
def check_sensitive(keyword1,keyword2):
    app_data = check_tocken()
    appid = app_data['appid']
    secret = app_data['secret']
    access_token = app_data['access_token']
    params = {
        'content': keyword1+keyword2
    }
    path = 'https://api.weixin.qq.com/wxa/msg_sec_check?access_token='+access_token
    headers = {'Charset': 'utf-8', 'Content-Type': 'application/json'}

    params = json.dumps(params, ensure_ascii=False)
    params = bytes(params, 'utf-8')
    req = urllib.request.Request(url=path, data=params, headers=headers, method='POST')
    res = urllib.request.urlopen(req).read()
    print(json.loads(res))
    return json.loads(res)['errcode']


@csrf_exempt
def SupAndDem(request):
    if request.method == 'POST':
        afferent_data = request.POST
        # 敏感词验证
        print(afferent_data['store_name'],afferent_data['content'])
        if afferent_data['store_name']+afferent_data['content'] != '':
            print('不为空')
            if check_sensitive(afferent_data['store_name'],afferent_data['content']) != 0 :
                return JsonResponse({"msg": "内容涉及敏感词！", "status_code": "401"}, status=status.HTTP_201_CREATED)
            else:
                if afferent_data['type'] == '1':
                    this_store = afferent_data['store_name']
                else:
                    this_store = ''
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
                    s_subtime=afferent_data['subtime'],
                    store_name=this_store
                )
                goods_arr = ast.literal_eval(afferent_data['goods'])
                for index, value in enumerate(goods_arr):
                    Material.objects.create(
                        m_id=demand,
                        type=index,
                        goods_name=goods_arr[index]['goods_name'],
                        count=goods_arr[index]['num_or_price']
                    )
                return JsonResponse({"msg": "操作成功！", "status_code": "201"}, status=status.HTTP_201_CREATED)
        else:
            if afferent_data['type'] == '1':
                this_store = afferent_data['store_name']
            else:
                this_store = ''
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
                s_subtime=afferent_data['subtime'],
                store_name=this_store
            )
            goods_arr = ast.literal_eval(afferent_data['goods'])
            for index, value in enumerate(goods_arr):
                Material.objects.create(
                    m_id=demand,
                    type=index,
                    goods_name=goods_arr[index]['goods_name'],
                    count=goods_arr[index]['num_or_price']
                )
            return JsonResponse({"msg": "操作成功！", "status_code": "201"}, status=status.HTTP_201_CREATED)


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

        start_time = str(data['start_time'])
        end_time = str(data['end_time'])

        start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")

        max_lat, max_lot, min_lat, min_lot = get_lat_lon_range(latitude, longitude, km)

        # id__gte=724 >=724  ; id__lte=724 <=724
        queryset = Demand.objects.filter(s_lat__lte=max_lat, s_lon__lte=max_lot,
                                         s_lat__gte=min_lat, s_lon__gte=min_lot,
                                         s_subtime__range=(start_time, end_time)).order_by('-s_subtime')
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

        start_time = str(data['start_time'])
        end_time = str(data['end_time'])

        start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")

        # queryset = Demand.objects.filter(u_id=u_id).order_by('s_subtime')

        user = UserInfo.objects.get(open_id=u_id)
        queryset = Demand.objects.filter(u_id=user.id, s_subtime__range=(start_time, end_time)).order_by('-s_subtime')

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