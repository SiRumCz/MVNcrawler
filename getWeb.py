import time
import urllib
import undetected_chromedriver.v2 as uc
import requests
from requests import HTTPError
from selenium.webdriver.chrome.service import Service

from utils import get_random_agent
from urllib.request import urlopen


def getCookies():
    url = 'https://mvnrepository.com/'
    driver = uc.Chrome()
    try:
        with driver:
            driver.get(url)  # known url using cloudflare's "under attack mode"
        cookie_str = driver.get_cookie("cf_clearance")["value"]
        driver.quit()
        with open("cookie.txt", "w") as f:
            f.write(cookie_str)
        return cookie_str
    except:
        return getCookies()

# getCookies()
def getWebContent(url):
    """
    Get web content using tis url
    :param url:
    :return:content type: string
    """
    with open("cookie.txt", "r") as f:
        cookie = f.readline()
    headers = {
        # 'User-Agent': get_random_agent(),
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
        "cookie": "cf_clearance=" + cookie
    }
    time.sleep(0.2)
    req = urllib.request.Request(url=url, headers=headers)  # 这里要注意，必须使用url=url，headers=headers的格式，否则回报错，无法连接字符
    try:
        response = urllib.request.urlopen(req)  # 注意，这里要用req，不然就被添加useragent

        content = response.read().decode("UTF-8")

        response.close()

        return content
    except urllib.error.HTTPError as err:
        print(url + "   is a wrong url")
        code = err.code
        print(code)
        if code == 403 :
            return "403 FORBIDDEN"
        elif code == 503:
            getCookies()
            return getWebContent(url)
        elif code==404:
            return "EMPTY"
        else:
            return getWebContent(url)
    except:
        return getWebContent(url)

# getWebContent("https://mvnrepository.com/")
def getWebContent2(url):
    """
    Get web content using tis url
    :param url:
    :return:content type: string
    """
    with open("cookie.txt", "r") as f:
        cookie = f.readline()
    headers = {
        # 'User-Agent': get_random_agent(),
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
        "cookie": "cf_clearance=" + cookie
    }
    # time.sleep(0.1)
    req = urllib.request.Request(url=url, headers=headers)  # 这里要注意，必须使用url=url，headers=headers的格式，否则回报错，无法连接字符
    try:
        response = urllib.request.urlopen(req)  # 注意，这里要用req，不然就被添加useragent

        content = response.read().decode("UTF-8")

        response.close()

        return content
    except urllib.error.HTTPError as err:
        print(url + "   is a wrong url")
        code = err.code
        print(code)
        if code == 403 :
            return "403 FORBIDDEN"
        elif code == 503:
            getCookies()
            return getWebContent(url)
        elif code== 404:
            return "EMPTY"
        else:
            return getWebContent(url)
    except:
        return getWebContent(url)
# print(getWebContent("https://mvnrepository.com/artifact/be.yildiz-games/common-client/"))
# print(getWebContent("https://mvnrepository.com"))

# import json
# from selenium import webdriver
# import time
#
# url = 'https://mvnrepository.com/'
# driver = webdriver.Chrome(executable_path="D:\\anaconda\Lib\site-packages\selenium\webdriver\chrome\chromedriver.exe")
#
# driver.get(url)
# # 卡主浏览器 回车继续运行
# input('请手动登录')
#
# # 获取cookie并通过json模块将dict转换成str
# dictCookies = driver.get_cookies()   #  核心
# jsonCookies = json.dumps(dictCookies)
# print(jsonCookies)
# # 登录完成后将cookie保存到本地文件
# # with open('taobao.json','w') as f:
# #     f.write(jsonCookies)
# # time.sleep(3)
# driver.close()

# from selenium import webdriver
