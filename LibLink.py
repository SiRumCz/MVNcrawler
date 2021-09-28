import re

import requests

from utils import strChange


def easyGetLibLink(g_list):
    '''
    after getting all the href from "https://repo1.maven.org/maven2/", remove the version href in last level
    :param g_list:
    :return:
    '''
    libLink = []
    for i in g_list:
        obj = re.compile(
            r'(?P<gId>.*)/(?P<aId>.*?)/.*?/',
            re.S)
        result = obj.finditer(i[0])
        for it in result:
            gId = it.group('gId')
            aId = it.group('aId')
            link = gId + "/" + aId
            libLink.append(link)
    libLink = list(set(libLink))
    return libLink


def getLibLink(g_list):
    '''
    after getting all the href from "https://repo1.maven.org/maven2/", search them with MVN API and check with
    "easyGetLibLink(g_list)" to get their href
    :param g_list:
    :return:
    '''
    groupId = ""
    artifactId = ''
    libLink1 = []
    for i in g_list:
        url1 = f"https://search.maven.org/solrsearch/select?q={i[1]}"
        user_data = requests.get(url1).json()
        obj = re.compile(
            r'(?P<gId>.*)/(?P<aId>.*?)/.*?/',
            re.S)
        result = obj.finditer(i[0])
        for it in result:
            gId = strChange(it.group('gId'), "/", ".")
            aId = it.group('aId')
        # print(gId, aId)
        for j in range(0, len(user_data['response']['docs'])):
            if (user_data['response']['docs'][j]).get('g') == gId:
                groupId = strChange(gId, '.', '/')
            if (user_data['response']['docs'][j]).get('a') == aId:
                artifactId = aId
        link = groupId + "/" + artifactId
        # print(link)
        libLink1.append(link)
    libLink = list(set(libLink1))
    return libLink


# xy = [['cl/daplay/jfun/1.0.0/', 'daplay.jfun.1.0.0'], ['cl/daplay/jrut/1.0.0/', 'daplay.jrut.1.0.0'],
#       ['cl/daplay/jrut/1.0.1/', 'daplay.jrut.1.0.1'], ['cl/daplay/jsurbtc/1.0.0/', 'daplay.jsurbtc.1.0.0']]
#
# print(easyGetLibLink(xy))
