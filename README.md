### 急物帮 后台服务 API
![](https://img.shields.io/badge/platform-CentOS7-green.svg)  ![](https://img.shields.io/badge/language-python3.6-green.svg)  ![](https://img.shields.io/badge/framework-Django-green.svg) ![](https://img.shields.io/badge/framework-uWSGI-green.svg) ![](https://img.shields.io/badge/framework-Nginx-green.svg) ![](https://img.shields.io/badge/version-v1.0-green.svg) 


# 后台启动步骤

# 1.进入项目目录：
```
cd /root/code/wuhan_server_api
```
# 2. 激活虚拟环境
```
conda activate wuhan
```

# 3. 启动uwsgi服务




## 3.1 前台运行命令
```
uwsgi --ini app_server_uwsgi.ini 
```
## 3.2 后台运行命令
```
nohup uwsgi --ini app_server_uwsgi.ini &
```

### 查看api信息：
```
http://121.43.233.66/
```

----


## 表结构信息
https://docs.qq.com/sheet/DWFZXeEdobkFWT3lK?tab=BB08J2&c=D54A0A0

## 会议纪要
https://docs.qq.com/doc/DWHdSUWdOZWZCbm9E

# 分工
1. 注册 - 廖文
+ 判断是否有userid ,没有则存，有则跳过

2. 发布 - 李硕 
+ 供应表 外键->物品表
+ 物品表加一个type 口罩 消毒液


3. 首页状态 -罗杰
+ 经纬度 大于小于
+ 热门  5km+ 随机10条（供求表）
+ 最新  5km + 时间（供求表）
+ 我的  自己的提交信息（供求表）

4. 搜索-供应表
+ 商店  -  供求表+用户表 廖文
+ 消毒液 - 供求表+新加的物品表  罗杰
+ 口罩  - 供求表+新加的物品表  李硕


----

后台管理系统
```
http://121.43.233.66:8002/admin/
root 
hnuwulab 
```

服务器信息：
```
服务器:

121.43.233.66
root
hnu..1234


代码：
服务器路径
/root/code

github托管:
https://github.com/luojie1024/wuhan_server_api.git


外网访问链接：
http://121.43.233.66:8000/


运行环境：
/root/ide/anancoda3/envs/wuhan/bin/python
```
