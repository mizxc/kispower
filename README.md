# kispower介绍:个人知识管理系统
kispower是一个集成了：时间管理、知识管理、网址导航、博客相册，基于WEB的个人知识管理系统。
让你在积累知识的过程中，逐渐打造一个属于自己的个人展示网站：<http://www.kispower.cn>

体验Kispower网站首页：http://demo.kispower.cn

体验Kispower知识管理后台：http://demo.kispower.cn/kadmin

登录用户名：admin ,登录密码：520520

## 一、Kispower作为个人知识管理工具，有如下优点
1、知识以思维导图的方式组织，结构清晰。

2、知识节点的内容呈现方式多样，支持文本、图片、视频、链接、html代码。

3、生产的知识支持导入导出，还可以分享给需要的朋友，同时分享也会同步到Kispower的共享知识库（一个集合了大家的知识分享的地方）。

4、建立一个总的知识框架，然后通过超链接，链接到细分的知识图谱。这样所有的知识都用思维导图管理起来了。

## 二、Kispower的时间管理工具同样功能强大
1、时间管理以年计划、月计划、周计划、日计划，4个维度来规划时间，既有未雨绸缪的远期计划，又有活在当下的近期详细规划。

2、计划看板，详细的展示每个计划的任务列表，随时更新完成度。

3、日计划总结，周计划总结、月计划总结，年计划总结。有回顾才有成长。

## 三、Kispower的网站导航功能
1、跟一般导航网站差不多，只是所有展示的网站都是由自己收集分类。

2、日积月累，导航就像入口，通向远方，很有用，很有必要。

## 四、Kispower的相册与博客功能
1、收集展示图片，源于你对生活的热爱，很适合摄影师、艺术家

2、博客即写作，在个人知识管理的过程中，学到的整理的，可以在博客输出。

# kispower部署步骤如下：
### kispower = centos + nginx + uwsgi + mongodb + python37 + flask + bootstrap + jsmind...

## linux系统：centos7.5 centos8都可以，以centos8为例

### 1、创建用户
groupadd kispower

useradd -g kispower kispower

### 2、创建目录
在 /opt 目录下创建目录：kispower

在 /opt/kispower 目录下创建目录：nginx、backup、bin、data、etc、logs、mongodb、python37

Clone:https://github.com/mizxc/kispower.git 

修改 project/config.py:

WEBSITE_KISPOWER = 'http://www.kispower.cn'

改为自己的域名

上传project文件夹到 /opt/kispower 目录下

### 3、安装nginx
安装工具和库：yum -y install gcc-c++ pcre pcre-devel zlib zlib-devel openssl openssl-devel

下载nginx：wget -c https://nginx.org/download/nginx-1.17.8.tar.gz

解压:tar -zxvf nginx-1.17.8.tar.gz

编译源码到/opt/kispower/nginx:

./configure --user=kispower --group=kispower --prefix=/opt/kispower/nginx --with-http_v2_module --with-http_ssl_module --with-http_sub_module --with-http_stub_status_module --with-http_gzip_static_module --with-http_flv_module --with-http_mp4_module --with-pcre

make && make install

上传kispower项目etc目录下的nginx.conf 到 /opt/kispower/etc下，把server_name改成自己的域名。

### 4、安装python37
安装工具包：

yum install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel

yum -y install libffi-devel

下载python:
wget https://www.python.org/ftp/python/3.7.6/Python-3.7.6.tgz

编译源码到/opt/kispower/python37:

./configure --prefix=/opt/kispower/python37

make && make install

链接命令到系统目录:

ln -s /opt/kispower/python37/bin/python3 /usr/bin/python37

ln -s /opt/kispower/python37/bin/pip3 /usr/bin/pip37

安装python模块:requirements.txt在kispower目录下

pip37 install -r  requirements.txt

### 5、安装mongodb
wget https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-rhel80-4.2.3.tgz

直接解压到指定目录（/opt/kispower/mongodb），不用安装。

复制kispower项目etc目录下的mongodb.conf 到 /opt/kispower/etc 目录下

### 6、安装uwsgi
pip37 install uwsgi

复制kispower项目etc目录下的uwsgi.ini 到 /opt/kispower/etc 目录下

### 7、添加开机自启动，防火墙（80，8080端口开放，80端口转到8080）
编辑：vi /etc/rc.d/rc.local

添加如下内容：

source /etc/profile

source /home/kispower/.bashrc

service firewalld start

firewall-cmd --add-port=80/tcp

firewall-cmd --add-port=8080/tcp

firewall-cmd --add-forward-port=port=80:proto=tcp:toport=8080

cd /opt/kispower/nginx/sbin

su kispower -c "./nginx"

cd /opt/kispower/mongodb/bin

su kispower -c "./mongod -f /opt/kispower/etc/mongodb.conf"

cd /opt/kispower/python37/bin

su kispower -c "./uwsgi /opt/kispower/etc/uwsgi.ini"

### 8、添加定时任务
切换到kispower用户后操作：

su kispower

crontab -e

20 02 * * * source /home/kispower/.bashrc && /opt/kispower/python37/bin/python3 /opt/kispower/project/bin/crontab_log.py

30 02 * * * source /home/kispower/.bashrc && /opt/kispower/python37/bin/python3 /opt/kispower/project/bin/crontab_backup.py

40 02 * * * source /home/kispower/.bashrc && /opt/kispower/python37/bin/python3 /opt/kispower/project/bin/crontab_tag.py


### 9、添加环境变量：
vi /home/kispoer/.bashrc

添加如下内容：

export PYTHONPATH=/opt/kispower


### 10、设置/opt/kispower文件夹的所有权为：kispower用户
chown -R kispower.kispower /opt/kispower/

-----------------------------------------------------------------------------------------------
注：阿里云80端口配置：（好像安全组开放了，就可以了）

1、安全组开放80端口

后台实例-更多-网络和安全组-安全组配置

点击“配置规则”--“添加安全组规则”：

端口范围：80/80

授权对象：0.0.0.0/0

-----------------------------------------------------------------------------------------------
如有疑问，加我VX : overead





