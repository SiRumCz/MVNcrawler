import re

from getWeb import getWebContent


def getFirstHref(content):
    '''
    Get first level href and his title from "https://repo1.maven.org/maven2/"
    :param content:
    :return:
    '''
    obj1 = re.compile(r'<a(?P<main>.*)</pre>', re.S)
    main_content = obj1.findall(content)[0]
    obj = re.compile(
        r'<a href="(?P<groupHref>.*?)".*?>(?P<groupId>.*?)/</a>',
        re.S)

    groupOfLib = obj.findall(main_content)

    return groupOfLib


def getNextHref(repo_url, gp, g_list):
    '''
        Get next level href and his title from "https://repo1.maven.org/maven2/" and combine them with previous level href
    :param repo_url:
    :param gp:
    :param g_list:
    :return:
    '''
    gp1 = []
    for i in gp:
        g1_url = repo_url + i[0]
        # print(g1_url)
        group2_list = getFirstHref(getWebContent(g1_url))
        # print(group2_list)
        if len(group2_list):
            for j in group2_list:
                c_list = ['1', '2']
                c_list[0] = i[0] + j[0]
                c_list[1] = i[1] + '.' + j[1]
                gp1.append(c_list)
        else:
            g_list.append(i)
    # print(gp1)
    return gp1, g_list
