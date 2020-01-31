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


服务器配置信息：
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