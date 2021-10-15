import csv
import re
import time

import requests

from utils import strChange, duplicateDrop


def divideGroupArtifact(file, tofile):
    '''
    after getting all the href from "https://repo1.maven.org/maven2/", remove the version href in last level
    :param g_list:
    :return:
    '''
    # lst = ['1']
    with open(file)as f:
        g1_csv = csv.reader(f)
        for j in g1_csv:
            obj = re.compile(
                r'(?P<gId>.*)/(?P<aId>.*?)/',
                re.S)
            # print(j[0])
            result = obj.findall(j[0])
            # print(result[0])
            # result[0] = strChange(result[0], "/", ".")
            # lst.append(result)
            # for i in range(len(group1_list)):
            with open(tofile, 'a', newline='')as f:
                f_csv = csv.writer(f)
                # ls[0] = group1_list[i]
                # print(ls[0])
                f_csv.writerow(result[0])
    #         if len(lst) >= 1000:
    #             print(lst)
    #             # print(time.strftime('  %Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    #             with open(tofile, 'a', newline='')as f:
    #                 f_csv = csv.writer(f)
    #                 f_csv.writerows(lst)
    #             lst = []
    # with open(tofile, 'a', newline='')as f:
    #     f_csv = csv.writer(f)
    #     f_csv.writerows(lst)
    duplicateDrop(tofile)


# divideGroupArtifact("data/result1.csv", "data/result.csv")


def removeVersion(file, tofile):
    '''
    after getting all the href from "https://repo1.maven.org/maven2/", remove the version href in last level
    :param g_list:
    :return:
    '''
    lst = []
    with open(file)as f:
        g1_csv = csv.reader(f)
        for j in g1_csv:
            obj = re.compile(
                r'(?P<gId>.*/).*?/',
                re.S)
            result = obj.findall(j[0])
            # result[0] = strChange(result[0], "/", ".")
            lst.append(result)
            if len(lst) >= 1000:
                with open(tofile, 'a', newline='')as f:
                    f_csv = csv.writer(f)
                    f_csv.writerows(lst)
                lst = []
    with open(tofile, 'a', newline='')as f:
        f_csv = csv.writer(f)
        f_csv.writerows(lst)
    duplicateDrop(tofile)


# removeVersion("data/versionlib.csv","data/versionlib2.csv")

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
