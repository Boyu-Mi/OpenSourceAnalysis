# OpenSourceAnalysis-backend

[toc]

ZJU-SRE project

### 构建数据库：

先自己新建一个test数据库（也可以是别的，比如改成sre）

![image-20221209175750187](README.assets\image-20221209175750187.png)

随后打开Mysql的命令行

![image-20221209175525818](README.assets\image-20221209175525818.png)

输入如下

mysql> **use test**(或你自己建的别的数据库名)

mysql> **source *D:/Desktop/test.sql;***

其中test.sql的路径请以实际为准，且其中斜杠方向必须为/。



### 配置：

cd 到程序根目录

1. 安装virtualenv `pip install virtualenv` 

2. 创建虚拟环境 `env virtualenv env`

3. 激活虚拟环境env ，即运行这个文件： (直接命令行输入`d:/本项目绝对路径/venv/Scripts/activate.bat`也可)

    ![image-20221209180103752](README.assets\image-20221209180103752.png)

4. 安装项目依赖 `pip install -r requirements.txt` 

5. 加载云图所需包下载：

    python执行以下语句：

    import nltk
    nltk.download()

    会弹出一个

    ![img](https://img-blog.csdn.net/20180301144836834)

​	其中第2步的位置理论上可以任意然后设置环境变量，但我不知道为啥失败了，所以还是装在了D盘下（或其他有效位置，在找不到nltkdata的时候报错信息会显示它尝试搜索的路径列表）。

6. 修改config.py中的内容为你的数据库信息
7. 在根目录新建一个`token`（无拓展名）文件，里面内容为`token github_xxxxxxxxxxxxxxxxxxxxxx`，需要自己去申请一个github token以获得较多的访问次数。如果不做第7步，程序也是能跑的，但每小时请求次数有一定限制。

cd frontend

1. 执行`npm install`
2. 修改`frontend\src\App.js`中的`window.back_url = "http://127.0.0.1:5000"`为后端运行地址，在本机的话就不用改了



### 运行：

后端：

1. cd 根目录

2. 激活虚拟环境env ，即运行activate.bat文件： (直接命令行输入`d:/本项目绝对路径/venv/Scripts/activate.bat`也可)

3. `python app.py`

前端：

1. `cd frontend`
2. `npm start`
