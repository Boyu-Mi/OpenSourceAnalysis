# 基础接口

## Repos

- 基础的 repo 数据爬取

## Users

- 获取某个用户的信息，注意要获取其 organization 或者 company（这个做项目对比的时候要用到）

## Commit

- 基础的 commit 数据爬取
- 总的 commits，从项目建立之初按时间排序
    - 返回结果可以指定起始结束时间；
    - 可以指定计数最小时间单位；
    - 例如 2017.1 到 2018.1，最小统计单位为一个月
- commit 中不同贡献者代码提交次数
- commit 中不同贡献者排序，指出核心贡献者（可定一个数值，比如排序结果的前20%，返回数据格式JSON，字段自拟）

## Issue & Pull requests

- 基础的 issue，pullrequest 数据获取
- 拟定与设计相关的关键词，如 fix, add, remove 之类的词
- 可以直接获取label 为 **feature** 的issue
- 指定时间范围内 issues 的 Open 和 Closed 数量，按时间排序
    - 可以指定计数最小时间单位
- 指定时间范围内 pull requests 不同状态的数量（例如 Open 的数量、Closed 的数量等），按时间排序
    - 可以指定计数最小时间单位
- 对 issues 和 pull requests 用上面提到的设计相关关键词进行过滤，收集其具体内容

# Pytorch

## 对 Pytorch 项目的 stargazer, committer, issue 人数的 company 信息进⾏数据可视化
stargazer: https://api.github.com/repos/pytorch/pytorch/stargazers "organizations_url"
- 分别统计这三种角色所属公司的人数 https://api.github.com/users/suo/orgs，返回排序结果
- repos, commits 和 issues pull requests 的展示调用上面的接口

## 项目之间对比

- 调用上面接口

## 数据可用性

- 需要将爬到的数据保存在本地，然后表明是什么时候爬取的

## code style

可考虑将 app.py 拆分成

- flask_main.py：初始化配置，导入路由
- urls.py: 注册路由
- view.py: 实现函数

在向api.github.com发送请求时使用了大量重复的try-catch块，可考虑使用函数装饰器减少重复代码，增强可读性

