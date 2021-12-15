import csv
import glob
import re
import matplotlib.pyplot as plt
import pandas

from getWeb import getWebContent2


def getManDep():
    with open("CVE.txt") as f:
        main_content = f.read()
    # print(main_content)
    obj = re.compile(
        r'<tr>.*?<td.*?><.*?>(.*?)</a>.*?</tr>',
        re.S)

    manDep = obj.findall(main_content)

    return manDep


def getlist():
    with open("CVE.csv", 'a', newline='')as fw:
        f_csv = csv.writer(fw)
        for i in getManDep():
            r = []
            r.append(i)
            print(i)
            f_csv.writerow(r)
    return "CVE.csv"


def cpe(cve):
    url = "https://nvd.nist.gov/vuln/detail/" + cve + "/cpes?expandCpeRanges=true"
    # url = "https://nvd.nist.gov/vuln/detail/" + cve
    # print(url)
    content = getWebContent2(url)
    # with open("CVE-2012-1717.txt") as f:
    #     content =f.read()
    # print("2")
    # print(content)
    obj = re.compile(
        r'id="cveTreeJsonDataHidden"(.*?)>',
        re.S)
    mc = obj.findall(content)
    # print("1")
    if len(mc) != 0:
        main_content = mc[0]
    else:
        return [], []
    # print(main_content)
    obj = re.compile(
        r'(cpe:2\.3.*?\(excluding.*?&)',
        re.S)
    ex = obj.findall(main_content)
    fix = []
    if len(ex) != 0:
        for i in ex:
            obj = re.compile(
                r'(cpe:2\.3.*?)&',
                re.S)
            c = obj.findall(i)[-1]
            obj = re.compile(
                r'\(excluding\)(.*?)&',
                re.S)
            ver = obj.findall(i)[0]
            ver = ver.replace(" ", "")
            c = c.replace("*", ver, 1)
            if c not in fix:
                fix.append(c)
    obj = re.compile(
        r'(cpe:2\.3.*?)&',
        re.S)
    cpe_list = obj.findall(main_content)
    ls = []
    for i in cpe_list:
        if i not in ls:
            ls.append(i)
    # return fix
    return ls, fix


# r, q = cpe("CVE-2021-44228")
# print(len(r))
# for i in r:
#     print(i)
# print(len(q))
# for i in q:
#     print(i)
def search():
    with open("csv_out.csv")as f_o:
        n = csv.reader(f_o)
        num = len(list(n))
    with open("CVE.csv") as f:
        g = csv.reader(f)
        for line, i in enumerate(g):
            if line < num:
                continue
            file1 = "cve/impact/" + i[0] + "_impact.csv"
            file2 = "cve/fix/" + i[0] + "_fix.csv"
            r, q = cpe(i[0])
            with open(file1, 'a', newline='')as f1:
                f_csv = csv.writer(f1)
                for j in r:
                    x = [j]
                    # x.append(j)
                    # print(j)
                    f_csv.writerow(x)
            with open(file2, 'a', newline='')as f2:
                f_csv = csv.writer(f2)
                for j in q:
                    x = [j]
                    # x.append(j)
                    # print(j)
                    f_csv.writerow(x)
            with open("csv_out.csv", 'a', newline='') as f_out:
                out_csv = csv.writer(f_out)
                out_csv.writerow(i)


# search()


# r,q=cpe("a")
# r=cpe("a")
# file1 = "cve/impact/CVE-2012-1717_impact.csv"
# file2 = "cve/fix/CVE-2012-1717_fix.csv"
# with open(file1, 'a', newline='')as f1:
#     f_csv = csv.writer(f1)
#     for j in r:
#         x = [j]
#         # x.append(j)
#         # print(j)
#         f_csv.writerow(x)
# # with open(file2, 'a', newline='')as f2:
# #     f_csv = csv.writer(f2)
# #     for j in q:
# #         x = [j]
# #         # x.append(j)
# #         # print(j)
# #         f_csv.writerow(x)

file = "CVE-2021-44228_impact.csv"


# with open(file) as f:
#     data = csv.reader(f)
#     for i in data:
#         obj = re.compile(
#             r'cpe:2\.3:.*?:(.*?):(.*?):(.*?):',
#             re.S)
#         ver = obj.findall(i)[0]

def file_list(path):
    path1 = path + "\*.csv"
    csv_list = glob.glob(path1)  # 查看同文件夹下的csv文件数
    # print(u'共发现%s个CSV文件' % len(csv_list))
    ls = []
    for i in csv_list:
        ls.append(i.replace(path + "\\", ""))
    return ls


# r = file_list("cve\\fix")
# for i in r:
#     print(i)
def divide(file):
    fp = "cve/fix/" + file
    with open(fp) as f:
        data = csv.reader(f)
        for i in data:
            # print(i)
            obj = re.compile(
                r'cpe:2\.3:.*?:(.*?):(.*?):(.*?):',
                re.S)
            ver = obj.findall(i[0])
            print(ver)
            try:
                print(ver[0][2])
            except:
                print(file)
            if ver[0][2] != "*" and ver[0][2] != "-":
                with open("cve/fix1/" + file, 'a', newline='')as fw:
                    f_csv = csv.writer(fw)
                    f_csv.writerow(ver[0])

# r = file_list("cve\\impact")
# # print(r[1772])
# for i in r:
#     if r.index(i)!=1772:
#         pass
#     else:
#         # print(r.index(i))
#         divide(i)


# r = file_list("cve\\fix")
# # print(r[1772])
# for i in r:
#     # if i=="CVE-2020-1945_impact.csv":
#     if r.index(i)<0:
#     #     print(r.index(i))
#         pass
#     else:
#         # print(r.index(i))
#         divide(i)


# CVE-2019-12837_impact.csv
# with open("CVE.csv", 'a', newline='')as fw:
#     f_csv = csv.writer(fw)
#     for i in getManDep():
#         r = []
#         r.append(i)
#         print(i)
#         f_csv.writerow(r)
def duplicateDrop(file):
    data = pandas.read_csv(file, header=None)
    data.drop_duplicates(subset=None, keep="first", inplace=True)
    data.to_csv(file, index=False, header=False)

# csv_list = glob.glob("cve/fix1/*.csv")  # 查看同文件夹下的csv文件数
# print(u'共发现%s个CSV文件' % len(csv_list))
# print(u'正在处理............')
# for i in csv_list:  # 循环读取同文件夹下的csv文件
#     duplicateDrop(i)
# from pylab import *                                 #支持中文
# mpl.rcParams['font.sans-serif'] = ['SimHei']
names = ['5', '10', '15', '20', '25']
x = range(len(names))
print(x)
y = [0.855, 0.84, 0.835, 0.815, 0.81]
x2=range(0,3)
y1=[0.86,0.85,0.853]
#plt.plot(x, y, 'ro-')
#plt.plot(x, y1, 'bo-')
#pl.xlim(-1, 11)  # 限定横轴的范围
#pl.ylim(-1, 110)  # 限定纵轴的范围
plt.plot(x, y, marker='o', mec='r', mfc='w',label=u'y=x^2')
plt.plot(x2, y1, marker='*', ms=10,label=u'y=x^3')
plt.legend()
# plt.xticks(x, names, rotation=45)
plt.margins(0)
plt.subplots_adjust(bottom=0.15)
# plt.xlabel(x)
# plt.ylabel(y)
plt.title("A simple plot")

plt.show()
