import re

from getWeb import getWebContent


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
        r'<tr><td>.*?href=\"(?P<href>.*?)\" class=\"vbtn release\">(?P<version>.*?)</a>.*?>Central<.*?<td.*?>.*?(?P<usages>[0-9]+?)[<\n].*?</span></td><td>(?P<date>.*?)</td>',
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


def getDependencies(groupId, artifactId):
    mvn_url = "https://mvnrepository.com/artifact"
    url = mvn_url + "/" + groupId + "/" + artifactId + "/"
    versionList = getVersionDetail(getWebContent(url))
    print(versionList)
    for i in versionList:
        print(i[0])
        print(getComDep(getWebContent(url + i[1])))
        print(getRunDep(getWebContent(url + i[1])))
        print(getTestDep(getWebContent(url + i[1])))


groupId = "edu.uci.ics"
artifactId = "crawler4j"
getDependencies(groupId, artifactId)
