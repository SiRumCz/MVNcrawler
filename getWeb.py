import urllib

from requests import HTTPError

from utils import get_random_agent
from urllib.request import urlopen


def getWebContent(url):
    """
    Get web content using tis url
    :param url:
    :return:content type: string
    """
    headers = {
        'User-Agent': get_random_agent()}
    req = urllib.request.Request(url=url, headers=headers)  # 这里要注意，必须使用url=url，headers=headers的格式，否则回报错，无法连接字符

    try:
        response = urllib.request.urlopen(req)  # 注意，这里要用req，不然就被添加useragent

        content = response.read().decode("UTF-8")

        response.close()

        return content
    except urllib.error.HTTPError as err:
        print(url + "   is a wrong url")
        code = err.code
        if code == 403:
            return "403 FORBIDDEN"
        else:
            # print(code)
            return "EMPTY"


# print(getWebContent("https://mvnrepository.com/artifact/be.yildiz-games/common-client/1.0.1"))
# str=getWebContent("https://zhuanlan.zhihu.com/p/123")
# print(str)
