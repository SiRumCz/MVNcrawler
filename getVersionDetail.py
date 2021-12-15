import csv
import datetime
import os
import re
import time

from getWeb import getWebContent
from utils import strChange, get_FileSize


def getLastVersionDetail(content):
    '''
    Get last versions, its version herf and usages with a content of Web like "https://mvnrepository.com/artifact/xxxx"
    :param content:
    :return:
    '''
    obj = re.compile(
        r'Central.*?Date.*?href=\"(?P<href>.*?)\" class=\"vbtn release\">(?P<version>.*?)</a>.*?>Central<.*?<td.*?>.*?(?P<usages>[0-9]+?)[<\n].*?</td>',
        re.S)

    result = obj.finditer(content)

    return result


def getVersionDetail(groupId, artifactId):
    '''
    Get versions, its version herf and usages with a content of Web like "https://mvnrepository.com/artifact/xxxx"
    :param content:
    :return:
    '''
    res = []
    mvn_url = "https://mvnrepository.com/artifact"
    url = mvn_url + "/" + groupId + "/" + artifactId + "/"
    # print(url)
    content = getWebContent(url)
    # obj = re.compile(
    #     r'Used By<.*?<b>(.*?)artifacts',
    #     re.S)
    # usage = obj.findall(content)[0]
    # print(usage)
    obj = re.compile(
        r'<tbody>(.*)</tbody>',
        re.S)
    content = obj.findall(content)[0]
    # print(content)
    obj = re.compile(
        r'<tr><td.*?>.*?href=\"(?P<artifact>.*?)/(?P<version>.*?)\" class=\"vbtn.*?\">.*?</a>.*?<td.*?>.*?(?P<usages>[0-9,]+?)[<\n].*?</span></td><td>(?P<date>.*?)</td>',
        re.S)
    result = obj.findall(content)
    # print(result)
    for i in result:
        # print(i)
        i = list(i)
        i.insert(0, groupId)
        res.append(i)
    return res


def getGroupId(content):
    '''
    Get group ID with a content of Web like "https://mvnrepository.com/artifact/xxxx"
    :param content: type: str
    :return: groupOfLib[0]
    '''
    obj = re.compile(
        r'>Home</a> » .*?>(?P<groupId>.*?)</a> »',
        re.S)

    groupOfLib = obj.findall(content)

    return groupOfLib[0]


def getComDep(content):
    obj1 = re.compile(r'<h2>Compile Dependencies.*?<tbody>(?P<main>.*?</table>)', re.S)
    if len(obj1.findall(content)) == 0:
        return []
    main_content = obj1.findall(content)[0]
    obj = re.compile(
        r'<tr>.*?</picture>.*?>([a-zA-Z0-9._&#-]+?)<.*?>([a-zA-Z0-9._&#-]+?)<.*?>\n*([a-zA-Z0-9._&#-]+?)\n*<.*?\n*([a-zA-Z0-9._&#-]+?)\n*<.*?</tr>',
        re.S)

    compileDep = obj.findall(main_content)

    return compileDep


def getTestDep(content):
    obj1 = re.compile(r'<h2>Test Dependencies.*?<tbody>(?P<main>.*?)</table>', re.S)
    if len(obj1.findall(content)) == 0:
        return []
    main_content = obj1.findall(content)[0]
    obj = re.compile(
        r'<tr>.*?</picture>.*?>([a-zA-Z0-9._&#-]+?)<.*?>([a-zA-Z0-9._&#-]+?)<.*?>\n*([a-zA-Z0-9._&#-]+?)\n*<.*?\n*([a-zA-Z0-9._&#-]+?)\n*<.*?</tr>',
        re.S)

    testDep = obj.findall(main_content)

    return testDep


def getRunDep(content):
    obj1 = re.compile(r'<h2>Runtime Dependencies.*?<tbody>(?P<main>.*?)</table>', re.S)
    if len(obj1.findall(content)) == 0:
        return []
    main_content = obj1.findall(content)[0]
    obj = re.compile(
        r'<tr>.*?</picture>.*?>([a-zA-Z0-9._&#-]+?)<.*?>([a-zA-Z0-9._&#-]+?)<.*?>\n*([a-zA-Z0-9._&#-]+?)\n*<.*?\n*([a-zA-Z0-9._&#-]+?)\n*<.*?</tr>',
        re.S)

    runDep = obj.findall(main_content)

    return runDep


def getManDep(content):
    obj1 = re.compile(r'<h2>Managed Dependencies.*?<tbody>(?P<main>.*?)</table>', re.S)
    if len(obj1.findall(content)) == 0:
        return []
    main_content = obj1.findall(content)[0]
    obj = re.compile(
        r'<tr>.*?</picture>.*?>([a-zA-Z0-9._&#-]+?)<.*?>([a-zA-Z0-9._&#-]+?)<.*?>\n*([a-zA-Z0-9._&#-]+?)\n*<.*?\n*([a-zA-Z0-9._&#-]+?)\n*<.*?</tr>',
        re.S)

    manDep = obj.findall(main_content)

    return manDep


def getDependencies(groupId, artifactId):
    res = []
    mvn_url = "https://mvnrepository.com/artifact"
    group_url = mvn_url + "/" + groupId + "/"
    # url = mvn_url + "/" + groupId + "/" + artifactId + "/"
    # print("3333333 " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
    # print(group_url)
    versionList = getVersionDetail(groupId, artifactId)
    # print(versionList)
    for i in versionList:
        # print(i[2])
        # time.sleep(1.1)
        # print("44444444 " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
        obj = re.compile(
            r'<th>Date</th><td>\((.*?)\) </td>',
            re.S)
        # print(group_url + i[1] + i[2])
        flag = 1
        webResult = getWebContent(group_url + i[1] + "/" + i[2])
        # print(i)
        while flag:
            if webResult == "403 FORBIDDEN":
                time.sleep(600)
                webResult = getWebContent(group_url + i[1] + "/" + i[2])
            else:
                flag = 0
        if webResult == "EMPTY":
            with open("data1/wrongVersion.csv", 'a', newline='')as fw:
                f_csv = csv.writer(fw)
                # ls[0] = group1_list[i]
                # print(ls[0])
                f_csv.writerow(i)
        else:
            DATE = obj.findall(webResult)[0]
            result = getComDep(webResult) + getManDep(
                webResult) + getRunDep(
                webResult) + getTestDep(webResult)
            # print("555555555 " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
            # print(result)
            for j in result:
                j = list(j)
                # print(j)
                i[4] = DATE
                q = i + j
                # print(q)
                res.append(q)
    for t in range(0, 999):
        file_name = "data1/dependencies" + str(t) + ".csv"
        if get_FileSize(file_name) < 10:
            break
    with open(file_name, 'a', newline='')as f:
        f_csv = csv.writer(f)
        # ls[0] = group1_list[i]
        # print(ls[0])
        f_csv.writerows(res)
    return res


mvn_url = "https://mvnrepository.com/artifact"
groupId = "edu.uci.ics"
artifactId = "crawler4j"
version = "4.4.0"
url = mvn_url + "/" + groupId + "/" + artifactId + "/" + version


# print(getVersionDetail(groupId, artifactId))


# getDependencies(groupId, artifactId)
# print(getComDep(getWebContent(url)))
# print(getComDep2(getWebContent(url)))


def write(file, file_out):
    with open(file_out)as f_o:
        n = csv.reader(f_o)
        num = len(list(n))
    with open(file)as f:
        g1_csv = csv.reader(f)
        for line, j in enumerate(g1_csv):
            if line < num:
                continue
            # time.sleep(1.1)
            flag = 1
            webResult = getWebContent("https://mvnrepository.com/artifact/" + strChange(j[0], '/', '.') + "/" + j[
                1])
            while flag:
                if webResult == "403 FORBIDDEN":
                    # print(j[0] + "/" + j[1] + "403")
                    time.sleep(600)
                    webResult = getWebContent(
                        "https://mvnrepository.com/artifact/" + strChange(j[0], '/', '.') + "/" + j[
                            1])
                else:
                    # time.sleep(1.1)
                    flag = 0
            if webResult == "EMPTY":
                # print("error:", end='')
                # print(j)
                with open("data1/wrongGA.csv", 'a', newline='')as f:
                    f_csv = csv.writer(f)
                    # ls[0] = group1_list[i]
                    # print(ls[0])
                    f_csv.writerow(j)
            else:
                # time.sleep(1.1)
                # print("2222222 " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
                getDependencies(strChange(j[0], '/', '.'), j[1])
                # print("44444444 " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
            with open(file_out, 'a', newline='') as f_out:
                out_csv = csv.writer(f_out)
                out_csv.writerow(j)


# os.system('shutdown /s ')
# write("data/result/r.csv", "data/result/r_out.csv")
# write("data1/result.csv", "data1/result_out.csv")
# print(getDependencies("ch.epfl.lamp","scala-library"))
# with open("MDG_data/MDG_data.csv") as f:
#     data = csv.reader(f)
#     num = len(list(data))
