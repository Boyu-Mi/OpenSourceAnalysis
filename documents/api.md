### @app.route('/commit', methods=['GET', 'POST'])
def commit(request):
#### request body：
``` json
{
    "url":"https://github.com/QSCTech/zju-icicles", //要查询的仓库地址,字符串
    "num_layout":3  //展示的突出贡献者的数量，默认3，整数
}
```
#### response body：
除了success为bool, id和stargazers_count, forks_count, watchers_count为整型，其他都是字符串（或null）
``` json
    如果发生了各种错误
    {
        "message": "No url!"或"Invalid github repo ink!"或"Timeout!"或"Fail to get info!"
        "success": false
    },404
    如果正常运行
    {
        "success": true, 
        "message": "success!",
        "target": "用户名/仓库名",
        "id": content_id, 
        "url": "该仓库url", 
        "owner": "owner", 
        "avatar_url": "仓库拥有者头像url",
        "html_url": "仓库拥有者用户页url", 
        "description": "仓库description",
        "topics": "topics",
        "stargazers_count": 仓库stargazer数量, 
        "forks_count":fork数量,
        "watchers_count" :watcher数量,
        "created_at": "仓库创建时间created_at", 
        "commit_users": [
        //列表，里面分别是突出贡献者的信息，项数为min(num_layout, 提交者数)
            {
                "a_url": "提交者头像url",
                "url": "提交者用户页url",
                "user": "提交者用户名"
            },
            {
                "a_url": "...",
                "url": "...",
                "user": "..."
            },
            ...
        ],
        "date_newest": "最新提交时间,格式 2016-08-13T05:07:47Z"
    }, 200
```

### @app.route('/user', methods=['GET', 'POST'])
def user(request):
#### request body
``` json
{
    "user_name":"用户名"
}
```
#### response body
follower_number, id, public_repo_number为整型，success为bool，其他都是字符串（或null）
``` json
    如果发生了错误:
    {
        "message": "No user name!"或"Invalid github repo ink!"或"Timeout!"或"Fail to get info!"
        "success": false
    }, 404
    如果正常运行:
    {
        "avatar_url": "用户头像url",
        "company": null 或 "公司名", //挺多用户company信息没填，就是null
        "created_at": "创建时间，格式：2021-08-25T12:43:21Z",
        "follower_number": follower_number,
        "id": user_id,
        "message": "success!",
        "public_repo_number": public_repo_number,
        "success": true,
        "updated_at": "最后更新时间，格式：2022-11-04T14:40:23Z",
        "user_name": "用户名",
        "user_type": "用户类型",
        "user_url": "用户页url"
    }, 200
```

### @app.route('/user', methods=['GET', 'POST'])
def commit_from(request):
#### request body

``` json

```
#### response body
``` json

```

### @app.route('/user', methods=['GET', 'POST'])
def Contribution_from(request):
#### request body

``` json

```
#### response body
``` json

```