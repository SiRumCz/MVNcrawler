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


def getVersionDetail(content):
    '''
    Get versions, its version herf and usages with a content of Web like "https://mvnrepository.com/artifact/xxxx"
    :param content:
    :return:
    '''
    obj = re.compile(
        r'<tbody>(.*)</tbody>',
        re.S)
    content = obj.findall(content)[0]
    obj = re.compile(
        r'<tr><td.*?>.*?href=\"(?P<href>.*?)\" class=\"vbtn release.*?\">(?P<version>.*?)</a>.*?>Central<.*?<td.*?>.*?(?P<usages>[0-9]+?)[<\n].*?</span></td><td>(?P<date>.*?)</td>',
        re.S)

    result = obj.findall(content)
    return result


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
    obj1 = re.compile(r'(?P<main><h2>Compile Dependencies.*?</table>)', re.S)
    if len(obj1.findall(content)) == 0:
        return []
    main_content = obj1.findall(content)[0]
    obj = re.compile(
        r'<tr>.*?</td>.*?</td><td>.*?>(?P<groupId>.*?)</a>[<\n]»\n.*?>(?P<artifactId>.*?)</a></td>.*?<a.*?>\n(?P<version>.*?)</a>.*?</tr>',
        re.S)

    compileDep = obj.findall(main_content)

    return compileDep


def getTestDep(content):
    obj1 = re.compile(r'<h2>Test Dependencies(?P<main>.*?)</table>', re.S)
    if len(obj1.findall(content)) == 0:
        return []
    main_content = obj1.findall(content)[0]
    obj = re.compile(
        r'<tr>.*?</td>.*?</td><td>.*?>(?P<groupId>.*?)</a>[<\n]»\n.*?>(?P<artifactId>.*?)</a></td>.*?<a.*?>\n(?P<version>.*?)</a>.*?</tr>',
        re.S)

    testDep = obj.findall(main_content)

    return testDep


def getRunDep(content):
    obj1 = re.compile(r'<h2>Runtime Dependencies(?P<main>.*?)</table>', re.S)
    if len(obj1.findall(content)) == 0:
        return []
    main_content = obj1.findall(content)[0]
    obj = re.compile(
        r'<tr>.*?</td>.*?</td><td>.*?>(?P<groupId>.*?)</a>[<\n]»\n.*?>(?P<artifactId>.*?)</a></td>.*?<a.*?>\n(?P<version>.*?)</a>.*?</tr>',
        re.S)

    runDep = obj.findall(main_content)

    return runDep


def getManDep(content):
    obj1 = re.compile(r'<h2>Managed Dependencies(?P<main>.*?)</table>', re.S)
    if len(obj1.findall(content)) == 0:
        return []
    main_content = obj1.findall(content)[0]
    obj = re.compile(
        r'<tr>.*?</td>.*?</td><td>.*?>(?P<groupId>.*?)</a>[<\n]»\n.*?>(?P<artifactId>.*?)</a></td>.*?<a.*?>\n(?P<version>.*?)</a>.*?</tr>',
        re.S)

    manDep = obj.findall(main_content)

    return manDep


def getDependencies(groupId, artifactId):
    mvn_url = "https://mvnrepository.com/artifact"
    url = mvn_url + "/" + groupId + "/" + artifactId + "/"
    versionList = getVersionDetail(getWebContent(url))
    # print(versionList)
    for i in versionList:
        print(i[0])
        time.sleep(1)
        print(getComDep(getWebContent(url + i[1])))
        print(getManDep(getWebContent(url + i[1])))
        print(getRunDep(getWebContent(url + i[1])))
        print(getTestDep(getWebContent(url + i[1])))


# groupId = "edu.uci.ics"
# artifactId = "crawler4j"
# getDependencies(groupId, artifactId)
def checkUrl(file):
    with open(file)as f:
        g1_csv = csv.reader(f)
        for j in g1_csv:
            time.sleep(1)
            if getWebContent("https://mvnrepository.com/artifact/" + strChange(j[0], "/", ".") + "/" + j[1]) == "EMPTY":
                print("error:", end='')
                print(j)
                # with open("data/wrongGA.csv", 'a', newline='')as f:
                #     f_csv = csv.writer(f)
                #     # ls[0] = group1_list[i]
                #     # print(ls[0])
                #     f_csv.writerow(j)
            else:
                getDependencies(strChange(j[0], "/", "."), j[1])


checkUrl("data/result.csv")
# print(getVersionDetail(getWebContent("https://mvnrepository.com/artifact/acegisecurity/acegi-security")))
