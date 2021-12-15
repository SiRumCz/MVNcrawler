import csv
import glob
import re
import time

from getVersionDetail import getVersionDetail, getDependencies, getTestDep, getRunDep, getComDep, getManDep
from getWeb import getWebContent
from utils import get_FileSize


def getDep2(g, a, v):
    result = []
    content = getWebContent("https://mvnrepository.com/artifact" + "/" + g + "/" + a + "/" + v)
    obj1 = re.compile(r'<h2>.*?Dependencies.*?<tbody>(.*?)</table>', re.S)
    main_content = obj1.findall(content)
    if len(main_content) == 0:
        return []
    obj = re.compile(
        r'<tr>.*?</picture>.*?>([a-zA-Z0-9._&#-]+?)<.*?>([a-zA-Z0-9._&#-]+?)<.*?>\n*([a-zA-Z0-9._&#-]+?)\n*<.*?\n*[a-zA-Z0-9._&#-]+?\n*<.*?</tr>',
        re.S)
    for j in main_content:
        Dep = obj.findall(j)
        for i in Dep:
            result.append(list(i))
    return result


def getDep(g, a, v):
    result = []

    content = getWebContent("https://mvnrepository.com/artifact" + "/" + g + "/" + a + "/" + v)
    # print(content)
    obj1 = re.compile(r'<h2>.*?Dependencies.*?<tbody>(.*?)</table>', re.S)
    main_content = obj1.findall(content)
    # print(main_content)
    # print(len(main_content))
    if len(main_content) == 0:
        return []
    obj = re.compile(
        r'<tr>.*?<td.*?<td.*?<td(.*?<td.*?)<td.*?</tr>',
        re.S)
    for j in main_content:
        Dep = obj.findall(j)
        # print(Dep)
        # print(len(Dep))
        for k in Dep:
            str = ""
            o = re.compile(
                r'>(.*?)<',
                re.S)
            m = o.findall(k)
            # print(m)
            for t in m:
                str = str + t
            # print(str)
            str = str.replace("»", "")
            str = str.replace("(optional)", "")
            # print(str)
            # to_one_line = ' '.join(str.split())
            res = str.split()
            result.append(res)
            # print(IP_LIST)
            # num=0
            # for s in str:
            #     if s =="\n":
            #         num=num+1
            # print(num)
        # for i in Dep:
        #     result.append(list(i))
    return result


# r = getDep("com.google.guava","guava","28.1-jre")
# print(r)

# print(len(r))
# print(r)
# org.scala-lang/scalap/2.13.5

def depen(g, a, v, res, dep, max_dep):
    dept = getDep(g, a, v)
    lst1 = []
    for j in dept:
        if j not in res:
            lst1.append(j)
    # print(lst1)
    if len(lst1) != 0:
        dep = dep + 1
        # for k in lst1:
        #     k = [k,depth]
        if max_dep < dep:
            max_dep = dep
        # res.extend(lst1)
        for i in lst1:
            res.append([i, dep])
            # print(i)
            if len(i) == 3:
                res, max_dep = depen(i[0], i[1],
                                     i[2].replace("[", '').replace(",", "").replace("(", "").replace(")", "").replace(
                                         "]", ""), res, dep, max_dep)
    return res, max_dep


# res=[]
# r = depen("org.springframework","spring-core","5.1.20.RELEASE",res)
# print(r)
# print(depen("junit", "junit","4.13.1",res))
# print(depen("com.fasterxml.jackson.core", "jackson-databind", "2.13.0",res))


# for i in r:
#     print(i)


def dfs(g, a):
    res = []
    mvn_url = "https://mvnrepository.com/artifact"
    group_url = mvn_url + "/" + g + "/"
    # url = mvn_url + "/" + groupId + "/" + artifactId + "/"
    # print("3333333 " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
    # print(group_url)
    versionList = getVersionDetail(g, a)
    # print(versionList)
    for i in versionList:
        print(i[2])
        # time.sleep(1.1)
        # print("44444444 " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
        obj = re.compile(
            r'<th>Date</th><td>\((.*?)\) </td>',
            re.S)
        # print(group_url + i[1] + i[2])
        # flag = 1
        webResult = getWebContent(
            group_url + i[1] + "/" + i[2].replace("[", '').replace(",", "").replace("(", "").replace(")", "").replace(
                "]", ""))
        # print(i)
        # while flag:
        #     if webResult == "403 FORBIDDEN":
        #         time.sleep(600)
        #         webResult = getWebContent(group_url + i[1] + "/" + i[2])
        #     else:
        #         flag = 0
        if webResult == "EMPTY":
            with open("data/error1-2/wrongVersion.csv", 'a', newline='')as fw:
                f_csv = csv.writer(fw)
                # ls[0] = group1_list[i]
                # print(ls[0])
                f_csv.writerow(i)
        else:
            DATE = obj.findall(webResult)[0]
            res = []
            direct = len(getDep(g, i[1], i[2]))
            l,m=depen(g, i[1], i[2], res, 0, 0)
            total = len(l)
            i[4] = DATE
            i.append(direct)
            i.append(total)
            i.append(m)
            # print(i)
            # print("555555555 " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
            # print(result)
    print(versionList)
    file_name = g + "_" + a + ".csv"
    with open("top_data1/" + file_name, 'a', newline='')as f:
        f_csv = csv.writer(f)
        # ls[0] = group1_list[i]
        # print(ls[0])
        f_csv.writerows(versionList)
    return versionList
    #         for j in result:
    #             j = list(j)
    #             # print(j)
    #             i[4] = DATE
    #             q = i + j
    #             # print(q)
    #             res.append(q)
    # for t in range(0, 999):
    #     file_name = "data/dependencies/dependencies" + str(t) + ".csv"
    #     if get_FileSize(file_name) < 10:
    #         break


# r = getVersionDetail("junit", "junit")
# r = dfs("org.scala-lang","scala-library")

# for i in r:
#     print(i)
def toplist(p):
    content = getWebContent("https://mvnrepository.com/popular?p=" + str(p))
    obj = re.compile(
        r'</h1>(.*?)class="search-nav">',
        re.S)
    content = obj.findall(content)[0]
    obj = re.compile(
        r'class="im-subtitle">.*?>(.*?)</a>.*?>(.*?)</a>.*?</p>',
        re.S)
    result = obj.findall(content)
    print(result)
    print(len(result))
    return result


# r = toplist(6)
#
# with open("top_data1/top.csv", 'a', newline='')as f:
#     f_csv = csv.writer(f)
#     # ls[0] = group1_list[i]
#     # print(ls[0])
#     f_csv.writerows(r)

with open("top_data1/top.csv")as f:
    data = csv.reader(f)
    # for i,eum in data:
    num = len(glob.glob(pathname='top_data1/*.csv'))
    # print(num)
    for line, i in enumerate(data):
        # print(line)
        if line < num - 1:
            continue
        print(i[0])
        dfs(i[0], i[1])


def file_list(path):
    path1 = path + "\*.csv"
    csv_list = glob.glob(path1)  # 查看同文件夹下的csv文件数
    # print(u'共发现%s个CSV文件' % len(csv_list))
    ls = []
    for i in csv_list:
        ls.append(i.replace(path + "\\", ""))
    return ls

# r = file_list("top_data")
# for i in r:
#     print(i)
