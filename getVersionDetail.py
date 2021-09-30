import re


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
