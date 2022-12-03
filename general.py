
def getApiUrl(url, parameter):
    """
    从仓库url中获取仓库相关api查询地址
    :param parameter:
    :param url: 仓库地址
    :return: api地址
    """
    assert parameter in ['', 'commits', 'contributors', 'issues']
    u_list = url.split('/')
    return 'https://api.github.com/repos/' + u_list[-2] + '/' + u_list[-1] + '/' + parameter


def getRepoInfo(url):
    """
    :param url: 仓库地址
    :return: 仓库名和owner用户名
    """
    u_list = url.split('/')
    return u_list[-2], u_list[-1]


