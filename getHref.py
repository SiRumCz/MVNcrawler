import csv
import os
import re
import time

from LibLink import removeVersion, divideGroupArtifact
from getWeb import getWebContent
from utils import duplicateDrop, delete_empty_rows, mergeCsv


def getFirstHref(content):
    '''
    Get first level href and his title from "https://repo1.maven.org/maven2/"
    :param content:
    :return:
    '''
    if content == "EMPTY":
        return "EMPTY"
    obj = re.compile(
        r'.*"(?P<pom>.*?\.pom)">.*?<',
        re.S)
    pom = obj.findall(content)
    # print(len(pom))
    if len(pom) != 0:
        return "VERSIONLIB"
    obj1 = re.compile(r'<pre.*?\.\..*?</a>(?P<main>.*)</pre>', re.S)
    main_content = obj1.findall(content)
    # print(main_content)
    if len(main_content) != 0 or main_content[0] != '\n\n':
        mainContent = obj1.findall(content)[0]
        obj = re.compile(
            r'<a href="(?P<groupHref>.*?/)".*?>.*?/</a>',
            re.S)
        groupOfLib = obj.findall(mainContent)
        # print(groupOfLib)
        if len(groupOfLib):
            return groupOfLib
        else:
            return "EMPTYDIR"
    else:
        return "EMPTY"


def getFirstHref2(content):
    '''
    Get first level href and his title from "https://repo1.maven.org/maven2/"
    :param content:
    :return:
    '''
    if content == "EMPTY":
        return "EMPTY"
    obj1 = re.compile(r'<pre.*?\.\..*?</a>(?P<main>.*)</pre>', re.S)
    main_content = obj1.findall(content)
    # print(main_content)
    if len(main_content) != 0 or main_content[0] != '\n\n':
        mainContent = obj1.findall(content)[0]
        obj = re.compile(
            r'<a href="(?P<groupHref>.*?/)".*?>.*?/</a>',
            re.S)
        groupOfLib = obj.findall(mainContent)
        # print(groupOfLib)
        if len(groupOfLib):
            return groupOfLib
        else:
            return "EMPTYDIR"
    else:
        return "EMPTY"


def goodGetFirstHref(content):
    '''
    Get first level href and his title from "https://repo1.maven.org/maven2/"
    :param content:
    :return:
    '''
    if content == "EMPTY":
        return "EMPTY"
    obj = re.compile(
        r'(maven-metadata\.xml)',
        re.S)
    final = obj.findall(content)
    # print(len(pom))
    if len(final) != 0:
        return []
    obj1 = re.compile(r'<pre.*?\.\..*?</a>(?P<main>.*)</pre>', re.S)
    main_content = obj1.findall(content)
    # print(main_content)
    if len(main_content) != 0 and main_content[0] != '\n\n':
        mainContent = obj1.findall(content)[0]
        obj = re.compile(
            r'<a href="(?P<groupHref>.*?/)".*?>.*?/</a>',
            re.S)
        groupOfLib = obj.findall(mainContent)
        # print(groupOfLib)
        if len(groupOfLib):
            return groupOfLib
        else:
            obj = re.compile(
                r'.*"(?P<jar>.*?\.jar)">.*?<',
                re.S)
            jar = obj.findall(mainContent)
            if len(jar) != 0:
                return "VERSIONLIB"
            else:
                obj = re.compile(
                    r'.*"(?P<pom>.*?\.pom)">.*?<',
                    re.S)
                pom = obj.findall(mainContent)
                # print(len(pom))
                if len(pom) != 0:
                    return "VERSIONLIB"
                else:
                    return "EMPTYDIR"
    else:
        return "EMPTYDIR"


# print(goodGetFirstHref(getWebContent("https://repo1.maven.org/maven2/HTTPClient/HTTPClient/")))

def badGetFirstHref(content):
    '''
    Get first level href and his title from "https://repo1.maven.org/maven2/"
    :param content:
    :param content:
    :return:
    '''
    if content == "EMPTY":
        return "EMPTY"
    obj1 = re.compile(r'<pre.*?\.\..*?</a>(?P<main>.*)</pre>', re.S)
    main_content = obj1.findall(content)
    # print(main_content)
    if len(main_content) != 0 and main_content[0] != '\n\n':
        mainContent = obj1.findall(content)[0]
        obj = re.compile(
            r'<a href="(?P<groupHref>.*?)".*?>.*?/</a>',
            re.S)
        groupOfLib = obj.findall(mainContent)
        # print(groupOfLib)
        if len(groupOfLib) != 0:
            return groupOfLib
        else:
            obj = re.compile(
                r'(maven-metadata\.xml)',
                re.S)
            final = obj.findall(content)
            # print(len(pom))
            if len(final) != 0:
                return []
            else:
                obj = re.compile(
                    r'.*"(?P<jar>.*?\.jar)">.*?<',
                    re.S)
                jar = obj.findall(mainContent)
                if len(jar) != 0:
                    return "VERSIONLIB"
                else:
                    obj = re.compile(
                        r'.*"(?P<pom>.*?\.pom)">.*?<',
                        re.S)
                    pom = obj.findall(mainContent)
                    # print(len(pom))
                    if len(pom) != 0:
                        return "VERSIONLIB"
                    else:
                        return "EMPTYDIR"
    else:
        return "EMPTY"


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


def writeNextHrefToCsvE(repo_url, gp, lst, lstFinal):
    # begin = time.time()
    g1_url = repo_url + gp[0]
    # print(g1_url)

    if getFirstHref(getWebContent(g1_url)) == "EMPTY":
        return ""
    else:
        group2_list = getFirstHref(getWebContent(g1_url))
        # print(group2_list)
        # print(group2_list)
        if len(group2_list):
            for j in group2_list:
                c_list = ['1']
                c_list[0] = gp[0] + j
                # print("clist:", c_list)
                lst.append(c_list)
                # print("lst=", end='')
                # print(lst)
        else:
            lstFinal.append(gp)
            # print("lstFinal=", end='')
            # print(lstFinal)
    # end = time.time()
    # print('check ' + gp[0] + ' time is %d m seconds ' % (int(round((end-begin) * 1000))))


def badWriteNextHrefToCsvE(repo_url, gp, lst, lstFinal):
    # begin = time.time()
    g1_url = repo_url + gp[0]
    # print(g1_url)

    ls = ['1']
    if goodGetFirstHref(getWebContent(g1_url)) == "EMPTY":
        try:
            with open('data/emptyURL.csv', 'a', newline='')as f:
                f_csv = csv.writer(f)
                for i in range(len(gp)):
                    ls[0] = gp[i]
                    # print(ls[0])
                    f_csv.writerow(ls)
        except UnicodeEncodeError:
            pass
    elif goodGetFirstHref(getWebContent(g1_url)) == "VERSIONLIB":
        try:
            with open('data/versionlib.csv', 'a', newline='')as f:
                f_csv = csv.writer(f)
                for i in range(len(gp)):
                    ls[0] = gp[i]
                    # print(ls[0])
                    f_csv.writerow(ls)
        except UnicodeEncodeError:
            pass
    elif goodGetFirstHref(getWebContent(g1_url)) == "EMPTYDIR":
        try:
            with open('data/emptylib.csv', 'a', newline='')as f:
                f_csv = csv.writer(f)
                for i in range(len(gp)):
                    ls[0] = gp[i]
                    # print(ls[0])
                    f_csv.writerow(ls)
        except UnicodeEncodeError:
            pass
    else:
        group2_list = badGetFirstHref(getWebContent(g1_url))
        # print(group2_list)
        # print(group2_list)
        if len(group2_list):
            for j in group2_list:
                c_list = ['1']
                c_list[0] = gp[0] + j
                # print("clist:", c_list)
                lst.append(c_list)
                # print("lst=", end='')
                # print(lst)
        else:
            lstFinal.append(gp)


def goodWriteNextHrefToCsvE(repo_url, gp, lst, lstFinal):
    # begin = time.time()
    g1_url = repo_url + gp[0]
    # print(g1_url)
    ls = ['1']
    if goodGetFirstHref(getWebContent(g1_url)) == "EMPTY":
        try:
            with open('data/emptyURL.csv', 'a', newline='')as f:
                f_csv = csv.writer(f)
                for i in range(len(gp)):
                    ls[0] = gp[i]
                    # print(ls[0])
                    f_csv.writerow(ls)
        except UnicodeEncodeError:
            pass
    elif goodGetFirstHref(getWebContent(g1_url)) == "VERSIONLIB":
        try:
            with open('data/versionlib.csv', 'a', newline='')as f:
                f_csv = csv.writer(f)
                for i in range(len(gp)):
                    ls[0] = gp[i]
                    # print(ls[0])
                    f_csv.writerow(ls)
        except UnicodeEncodeError:
            pass
    elif goodGetFirstHref(getWebContent(g1_url)) == "EMPTYDIR":
        try:
            with open('data/emptylib.csv', 'a', newline='')as f:
                f_csv = csv.writer(f)
                for i in range(len(gp)):
                    ls[0] = gp[i]
                    # print(ls[0])
                    f_csv.writerow(ls)
        except UnicodeEncodeError:
            pass
    else:
        group2_list = goodGetFirstHref(getWebContent(g1_url))
        # print(group2_list)
        # print(group2_list)
        if len(group2_list):
            for j in group2_list:
                c_list = ['1']
                c_list[0] = gp[0] + j
                # print("clist:", c_list)
                lst.append(c_list)
                # print("lst=", end='')
                # print(lst)
        else:
            lstFinal.append(gp)
            # print(lstFinal)


def reWriteNextHrefToCsvE(repo_url, gp, lst, lstFinal):
    # begin = time.time()
    g1_url = repo_url + gp[0]
    # print(g1_url)
    ls = ['1']
    # print(getFirstHref(getWebContent(g1_url)))
    if getFirstHref(getWebContent(g1_url)) == "EMPTY":
        try:
            with open('data/error/emptyURL.csv', 'a', newline='')as f:
                f_csv = csv.writer(f)
                for i in range(len(gp)):
                    ls[0] = gp[i]
                    # print(ls[0])
                    f_csv.writerow(ls)
        except UnicodeEncodeError:
            pass
    elif getFirstHref(getWebContent(g1_url)) == "VERSIONLIB":
        try:
            with open('data/error/versionlib.csv', 'a', newline='')as f:
                f_csv = csv.writer(f)
                for i in range(len(gp)):
                    ls[0] = gp[i]
                    # print(ls[0])
                    f_csv.writerow(ls)
        except UnicodeEncodeError:
            pass
    elif getFirstHref(getWebContent(g1_url)) == "EMPTYDIR":
        try:
            with open('data/error/versionlib.csv', 'a', newline='')as f:
                f_csv = csv.writer(f)
                for i in range(len(gp)):
                    ls[0] = gp[i]
                    # print(ls[0])
                    f_csv.writerow(ls)
        except UnicodeEncodeError:
            pass
    else:
        group2_list = getFirstHref(getWebContent(g1_url))
        # print(group2_list)
        # print(group2_list)
        if len(group2_list):
            for j in group2_list:
                c_list = ['1']
                c_list[0] = gp[0] + j
                # print("clist:", c_list)
                lst.append(c_list)
                # print("lst=", end='')
                # print(lst)
        else:
            lstFinal.append(gp)
            # print(lstFinal)


def reWriteNextHrefToCsvE2(repo_url, gp, lst, lstFinal):
    # begin = time.time()
    g1_url = repo_url + gp[0]
    # print(g1_url)
    ls = ['1']
    # print(getFirstHref(getWebContent(g1_url)))
    if getFirstHref2(getWebContent(g1_url)) == "EMPTY":
        try:
            with open('data/error/emptyURL.csv', 'a', newline='')as f:
                f_csv = csv.writer(f)
                for i in range(len(gp)):
                    ls[0] = gp[i]
                    # print(ls[0])
                    f_csv.writerow(ls)
        except UnicodeEncodeError:
            pass
    elif getFirstHref2(getWebContent(g1_url)) == "VERSIONLIB":
        try:
            with open('data/error/versionlib.csv', 'a', newline='')as f:
                f_csv = csv.writer(f)
                for i in range(len(gp)):
                    ls[0] = gp[i]
                    # print(ls[0])
                    f_csv.writerow(ls)
        except UnicodeEncodeError:
            pass
    elif getFirstHref2(getWebContent(g1_url)) == "EMPTYDIR":
        try:
            with open('data/error/versionlib.csv', 'a', newline='')as f:
                f_csv = csv.writer(f)
                for i in range(len(gp)):
                    ls[0] = gp[i]
                    # print(ls[0])
                    f_csv.writerow(ls)
        except UnicodeEncodeError:
            pass
    else:
        group2_list = getFirstHref2(getWebContent(g1_url))
        # print(group2_list)
        # print(group2_list)
        if len(group2_list):
            for j in group2_list:
                c_list = ['1']
                c_list[0] = gp[0] + j
                # print("clist:", c_list)
                lst.append(c_list)
                # print("lst=", end='')
                # print(lst)
        else:
            lstFinal.append(gp)
            # print(lstFinal)


def checkWrong(file):
    repo_url = "https://repo1.maven.org/maven2/"
    fileName = file
    lst = []
    lstFinal = []
    for i in range(0, 100):
        if i != 0:
            fileName = "data/error/" + str(i) + ".csv"
        file2 = "data/error/" + str(i + 1) + ".csv"
        if os.stat(fileName).st_size == 0:
            os.remove(fileName)
            break
        else:
            duplicateDrop(fileName)
            delete_empty_rows(fileName)
            with open(fileName)as f:
                g1_csv = csv.reader(f)
                if i > 2:
                    for j in g1_csv:
                        reWriteNextHrefToCsvE(repo_url, j, lst, lstFinal)
                        if len(lst) >= 100:
                            print("lst=", end='')
                            print(lst)
                            try:
                                with open(file2, 'a', newline='')as f:
                                    f_csv = csv.writer(f)
                                    f_csv.writerows(lst)
                                lst = []
                            except UnicodeEncodeError:
                                for k in lst:
                                    try:
                                        with open(file2, 'a', newline='')as f:
                                            f_csv = csv.writer(f)
                                            f_csv.writerow(k)

                                    except UnicodeEncodeError:
                                        print(k)
                                        lst[lst.index(k)] = ''
                                lst = []
                        else:
                            pass
                else:
                    for j in g1_csv:
                        reWriteNextHrefToCsvE2(repo_url, j, lst, lstFinal)
                        if len(lst) >= 100:
                            print("lst=", end='')
                            print(lst)
                            try:
                                with open(file2, 'a', newline='')as f:
                                    f_csv = csv.writer(f)
                                    f_csv.writerows(lst)
                                lst = []
                            except UnicodeEncodeError:
                                for k in lst:
                                    try:
                                        with open(file2, 'a', newline='')as f:
                                            f_csv = csv.writer(f)
                                            f_csv.writerow(k)

                                    except UnicodeEncodeError:
                                        print(k)
                                        lst[lst.index(k)] = ''
                                lst = []
                        else:
                            pass
        print("the last lst=", end='')
        print(lst)
        try:
            with open(file2, 'a', newline='')as f:
                f_csv = csv.writer(f)
                f_csv.writerows(lst)
            lst = []
        except UnicodeEncodeError:
            try:
                for k in lst:
                    with open(file2, 'a', newline='')as f:
                        f_csv = csv.writer(f)
                        f_csv.writerow(k)
                lst = []
            except UnicodeEncodeError:
                print(k)
                lst[lst.index(k)] = ''


# mergeCsv("data/wrongGA.csv", "data/error/wrongGA.csv")
# checkWrong("data/error/wrongGA.csv")
# removeVersion("data/error/versionlib.csv", "data/error/versionlib2.csv")
# divideGroupArtifact("data/error/versionlib2.csv", "data/result.csv")


# goodWriteNextHrefToCsvE("https://repo1.maven.org/maven2/", gp=["org.elasticsearch/elasticsearch/5.0.0-beta1/"], lst=[], lstFinal=[])
# print(goodGetFirstHref(getWebContent("https://repo1.maven.org/maven2/org.elasticsearch/elasticsearch/5.0.0-beta1/")))
# print(goodGetFirstHref(getWebContent("https://repo1.maven.org/maven2/org.elasticsearch/elasticsearch/")))
# print(goodGetFirstHref(getWebContent("https://repo1.maven.org/maven2/co/touchlab/android-arch-driver/")))
# print(goodGetFirstHref(getWebContent("https://repo1.maven.org/maven2/co/touchlab/")))

def recheckEmpty(repo_url, file):
    # begin = time.time()
    with open(file)as f:
        g1_csv = csv.reader(f)
        for j in g1_csv:
            g1_url = repo_url + j[0]
            # print(g1_url)
            ls = ['1']
            if goodGetFirstHref(getWebContent(g1_url)) == "EMPTY":
                try:
                    with open('data/emptyURL.csv', 'a', newline='')as f:
                        f_csv = csv.writer(f)
                        for i in range(len(j)):
                            ls[0] = j[i]
                            # print(ls[0])
                            f_csv.writerow(ls)
                except UnicodeEncodeError:
                    pass
            elif goodGetFirstHref(getWebContent(g1_url)) == "EMPTYDIR":
                try:
                    with open('data/emptyLib.csv', 'a', newline='')as f:
                        f_csv = csv.writer(f)
                        for i in range(len(j)):
                            ls[0] = j[i]
                            # print(ls[0])
                            f_csv.writerow(ls)
                except UnicodeEncodeError:
                    pass
            elif goodGetFirstHref(getWebContent(g1_url)) == "VERSIONLIB":
                try:
                    with open('data/versionlib.csv', 'a', newline='')as f:
                        f_csv = csv.writer(f)
                        for i in range(len(j)):
                            ls[0] = j[i]
                            # print(ls[0])
                            f_csv.writerow(ls)
                except UnicodeEncodeError:
                    pass

# repo_url = "https://repo1.maven.org/maven2/"
# for i in range(3, 4):
#     file = "data/" + str(i) + "-3.csv"
#     print("start：" + file + time.strftime('  %Y-%m-%d %H:%M:%S', time.localtime(time.time())))
#     recheckEmpty(repo_url, file)
#     print("end：" + file + time.strftime('  %Y-%m-%d %H:%M:%S', time.localtime(time.time())))

# def coutinueSearch(repo_url, begin, end, fileFinal, file2):
#     lst = []
#     lstFinal = []
#     for i in range(begin, end):
#         fileName = "data/divide3/3_" + str(i) + ".csv"
#         if os.path.exists(fileName):
#             with open(fileName)as f:
#                 g1_csv = csv.reader(f)
#                 begin = time.time()
#                 for j in g1_csv:
#                     # print(j)
#                     writeNextHrefToCsvE(repo_url, j, lst, lstFinal)
#                     # g1_csv.drop(i)
#                     if len(lst) >= 100:
#                         print("lst=", end='')
#                         print(lst)
#                         try:
#                             with open(file2, 'a', newline='')as f:
#                                 f_csv = csv.writer(f)
#                                 f_csv.writerows(lst)
#                             lst = []
#                         except UnicodeEncodeError:
#                             try:
#                                 for k in lst:
#                                     with open(file2, 'a', newline='')as f:
#                                         f_csv = csv.writer(f)
#                                         f_csv.writerow(k)
#                                 lst = []
#                             except UnicodeEncodeError:
#                                 print(k)
#                     else:
#                         pass
#                     if len(lstFinal) >= 100:
#                         print("lstFinal=", end='')
#                         print(lstFinal)
#                         try:
#                             with open(fileFinal, 'a', newline='')as f:
#                                 f_csv = csv.writer(f)
#                                 f_csv.writerows(lstFinal)
#                             lstFinal = []
#                         except UnicodeEncodeError:
#                             try:
#                                 for k in lstFinal:
#                                     with open(fileFinal, 'a', newline='')as f:
#                                         f_csv = csv.writer(f)
#                                         f_csv.writerow(k)
#                                 lstFinal = []
#                             except UnicodeEncodeError:
#                                 print(k)
#                     else:
#                         pass
#         else:
#             pass
#         end = time.time()
#         print(fileName + 'time is %d seconds ' % (end - begin))
#
#     print("the last lst=", end='')
#     print(lst)
#     try:
#         with open(file2, 'a', newline='')as f:
#             f_csv = csv.writer(f)
#             f_csv.writerows(lst)
#         lst = []
#     except UnicodeEncodeError:
#         try:
#             for k in lst:
#                 with open(file2, 'a', newline='')as f:
#                     f_csv = csv.writer(f)
#                     f_csv.writerow(k)
#             lst = []
#         except UnicodeEncodeError:
#             print(k)
#
#     print("the last lstFinal=", end='')
#     print(lstFinal)
#     try:
#         with open(fileFinal, 'a', newline='')as f:
#             f_csv = csv.writer(f)
#             f_csv.writerows(lstFinal)
#         lstFinal = []
#     except UnicodeEncodeError:
#         try:
#             for k in lstFinal:
#                 with open(fileFinal, 'a', newline='')as f:
#                     f_csv = csv.writer(f)
#                     f_csv.writerow(k)
#             lstFinal = []
#         except UnicodeEncodeError:
#             print(k)
#
#
# def badCoutinueSearch(repo_url, begin, end, fileFinal, file2):
#     lst = []
#     lstFinal = []
#     for i in range(begin, end):
#         fileName = "data/divide3/3_" + str(i) + ".csv"
#         if os.path.exists(fileName):
#             with open(fileName)as f:
#                 g1_csv = csv.reader(f)
#                 begin = time.time()
#                 for j in g1_csv:
#                     # print(j)
#                     writeNextHrefToCsvE(repo_url, j, lst, lstFinal)
#                     # g1_csv.drop(i)
#                     if len(lst) >= 100:
#                         print("lst=", end='')
#                         print(lst)
#                         try:
#                             with open(file2, 'a', newline='')as f:
#                                 f_csv = csv.writer(f)
#                                 f_csv.writerows(lst)
#                             lst = []
#                         except UnicodeEncodeError:
#                             try:
#                                 for k in lst:
#                                     with open(file2, 'a', newline='')as f:
#                                         f_csv = csv.writer(f)
#                                         f_csv.writerow(k)
#                                 lst = []
#                             except UnicodeEncodeError:
#                                 print(k)
#                     else:
#                         pass
#                     if len(lstFinal) >= 100:
#                         print("lstFinal=", end='')
#                         print(lstFinal)
#                         try:
#                             with open(fileFinal, 'a', newline='')as f:
#                                 f_csv = csv.writer(f)
#                                 f_csv.writerows(lstFinal)
#                             lstFinal = []
#                         except UnicodeEncodeError:
#                             try:
#                                 for k in lstFinal:
#                                     with open(fileFinal, 'a', newline='')as f:
#                                         f_csv = csv.writer(f)
#                                         f_csv.writerow(k)
#                                 lstFinal = []
#                             except UnicodeEncodeError:
#                                 print(k)
#                     else:
#                         pass
#         else:
#             pass
#         end = time.time()
#         print(fileName + 'time is %d seconds ' % (end - begin))
#
#     print("the last lst=", end='')
#     print(lst)
#     try:
#         with open(file2, 'a', newline='')as f:
#             f_csv = csv.writer(f)
#             f_csv.writerows(lst)
#         lst = []
#     except UnicodeEncodeError:
#         try:
#             for k in lst:
#                 with open(file2, 'a', newline='')as f:
#                     f_csv = csv.writer(f)
#                     f_csv.writerow(k)
#             lst = []
#         except UnicodeEncodeError:
#             print(k)
#
#     print("the last lstFinal=", end='')
#     print(lstFinal)
#     try:
#         with open(fileFinal, 'a', newline='')as f:
#             f_csv = csv.writer(f)
#             f_csv.writerows(lstFinal)
#         lstFinal = []
#     except UnicodeEncodeError:
#         try:
#             for k in lstFinal:
#                 with open(fileFinal, 'a', newline='')as f:
#                     f_csv = csv.writer(f)
#                     f_csv.writerow(k)
#             lstFinal = []
#         except UnicodeEncodeError:
#             print(k)

# repo_url = "https://repo1.maven.org/maven2/"
# group1_list = badGetFirstHref(getWebContent(repo_url))
# print(group1_list)
# ls=["ai/hyacinth/framework/core-service-admin-server/"]
#
# fileFinal = "data/group3.csv"
# lst = []
# lstFinal = []
# gp = ["co/touchlab/stately-iso-collections-linuxarm32hfp/0.10.0/",
#       "co.touchlab.stately-iso-collections-linuxarm32hfp.0.10.0"]
# writeNextHrefToCsvE(repo_url, gp, lst, lstFinal)
# print(lst)
# print(lstFinal)
# print(agetFirstHref(getWebContent("https://repo1.maven.org/maven2/com/cedarsoft/thirdparty/")))
# print(getFirstHref(getWebContent("https://repo1.maven.org/maven2/codehaus/")))
# begin=time.time()
# print(agetFirstHref(getWebContent("https://repo1.maven.org/maven2/co/touchlab/stately-iso-collections-linuxarm32hfp/0.10.0/")))
# end = time.time()
# print('time is %d m seconds ' % (int(round((end-begin) * 1000))))
# print(getWebContent("https://repo1.maven.org/maven2/codehaus/"))

# asdf(getWebContent("https://blog.csdn.net/weixin_45086637/article/details/92799127"))

# writeNextHrefToCsvE(repo_url,ls,[],[])
