import csv
import re
import time

from getWeb import getWebContent
from utils import strChange


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
    obj = re.compile(
        r'<tr><td.*?>.*?href=\"(?P<artifact>.*?)/(?P<version>.*?)\" class=\"vbtn.*?\">.*?</a>.*?>Central<.*?<td.*?>.*?(?P<usages>[0-9]+?)[<\n].*?</span></td><td>(?P<date>.*?)</td>',
        re.S)

    result = obj.findall(content)
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
    versionList = getVersionDetail(groupId, artifactId)
    # print(versionList)
    for i in versionList:
        # print(i[2])
        time.sleep(1.1)
        obj = re.compile(
            r'<th>Date</th><td>\((.*?)\) </td>',
            re.S)
        # print(group_url + i[1] + i[2])
        flag = 1
        while flag:
            if getWebContent(group_url + i[1] + "/" + i[2]) == "403 FORBIDDEN":
                # print(i[1] + "/" + i[2]+"403")
                time.sleep(60)
            else:
                break
        if getWebContent(group_url + i[1] + "/" + i[2]) == "EMPTY":
            with open("data/wrongVersion.csv", 'a', newline='')as fw:
                f_csv = csv.writer(fw)
                # ls[0] = group1_list[i]
                # print(ls[0])
                f_csv.writerow(i)
        else:
            DATE = obj.findall(getWebContent(group_url + i[1] + "/" + i[2]))[0]
            result = getComDep(getWebContent(group_url + i[1] + "/" + i[2])) + getManDep(
                getWebContent(group_url + i[1] + "/" + i[2])) + getRunDep(
                getWebContent(group_url + i[1] + "/" + i[2])) + getTestDep(getWebContent(group_url + i[1] + "/" + i[2]))
            # print(result)
            for j in result:
                j = list(j)
                # print(j)
                i[4] = DATE
                q = i + j
                # print(q)
                res.append(q)
    with open("data/dependencies.csv", 'a', newline='')as f:
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


def write(file):
    with open("data/result_out.csv")as f_o:
        n = csv.reader(f_o)
        num = len(list(n))
    with open(file)as f:
        g1_csv = csv.reader(f)
        for line, j in enumerate(g1_csv):
            if line < num:
                continue
            time.sleep(1.1)
            flag = 1
            while flag:
                if getWebContent("https://mvnrepository.com/artifact/" + strChange(j[0], "/", ".") + "/" + j[1]) == "403 FORBIDDEN":
                    # print(j[0] + "/" + j[1] + "403")
                    time.sleep(60)
                else:
                    break
            if getWebContent("https://mvnrepository.com/artifact/" + strChange(j[0], "/", ".") + "/" + j[1]) == "EMPTY":
                # print("error:", end='')
                # print(j)
                with open("data/wrongGA.csv", 'a', newline='')as f:
                    f_csv = csv.writer(f)
                    # ls[0] = group1_list[i]
                    # print(ls[0])
                    f_csv.writerow(j)
            else:
                getDependencies(strChange(j[0], "/", "."), j[1])
            with open("data/result_out.csv", 'a', newline='') as f_out:
                out_csv = csv.writer(f_out)
                out_csv.writerow(j)


write("data/result.csv")
# print(getVersionDetail(getWebContent("https://mvnrepository.com/artifact/activemq/activemq-container")))
