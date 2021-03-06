import csv
import glob
import random
import os
import re

import pandas as pd
import time

user_agent_list = [
    # Chrome
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
    # Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0'
]


def get_random_agent():
    return random.choice(user_agent_list)


def strChange(str1, a, b):
    str2 = ""
    for i in str1:
        if i == a:
            i = b
        str2 += i
    return str2


# ?????????csv????????????????????????csv??????

def mkSubFile(lines, srcName, sub):
    [des_filename, extname] = os.path.splitext(srcName)
    filename = des_filename + '_' + str(sub) + extname
    print('make file: %s' % filename)
    fout = open(filename, 'w')
    try:
        fout.writelines(lines)
        return sub + 1
    finally:
        fout.close()


def splitByLineCount(filename, count):
    fin = open(filename, encoding="utf-8")
    try:
        buf = []
        sub = 1
        for line in fin:
            buf.append(line)
            if len(buf) == count:
                sub = mkSubFile(buf, filename, sub)
                buf = []
        if len(buf) != 0:
            sub = mkSubFile(buf, filename, sub)
    finally:
        fin.close()

# splitByLineCount("data/result/result_1.csv",50000)

# ??????csv
def mergeCsv(paraFile, resultName):
    csv_list = glob.glob(paraFile)  # ????????????????????????csv?????????
    print(u'?????????%s???CSV??????' % len(csv_list))
    print(u'????????????............')
    for i in csv_list:  # ??????????????????????????????csv??????
        fr = open(i, 'rb').read()
        with open(resultName, 'ab') as f:  # ??????????????????result.csv
            f.write(fr)
    print(u'???????????????')


# ??????csv???????????????
def divideCsv(file, toFile):
    data = pd.read_csv(file, header=None)
    data.columns = ["A", "B"]
    data = data['A'].to_frame()
    data.to_csv(toFile, index=False, header=False)


# csv?????????????????????
def duplicateDrop(file):
    data = pd.read_csv(file, header=None)
    data.drop_duplicates(subset=None, keep="first", inplace=True)
    data.to_csv(file, index=False, header=False)


# ????????????
def delete_empty_rows(file_path):
    data = pd.read_csv(file_path, header=None)
    data.dropna(how="all", inplace=True)
    data.to_csv(file_path, index=False, header=False)


# ????????????csv?????????????????????????????????
def delRepeat(file1, file2, file3):
    df1 = pd.read_csv(file1, header=None)
    df2 = pd.read_csv(file2, header=None)
    # print(df2)
    frames = [df1, df2]
    # print(frames)
    data = pd.concat(frames, sort=False).reset_index(drop=True)
    data.drop_duplicates(keep=False, inplace=True)
    data.to_csv(file3, index=False, header=False)


# csv?????????N???
def keepNrows(file, n):
    data = pd.read_csv(file, header=None, nrows=n)
    data.to_csv(file, index=False, header=False)


# ???n???????????????csv
def readCsvFromNrow(file, n):
    with open(file)as f:
        data = csv.reader(f)
        # print(type(data))
        for line, i in enumerate(data):
            if line < n:
                continue
            else:
                print(i)
        #


def mergeCsv(file, tofile):
    '''
    after getting all the href from "https://repo1.maven.org/maven2/", remove the version href in last level
    :param g_list:
    :return:
    '''
    k = []
    with open(file)as f:
        g1_csv = csv.reader(f)
        for j in g1_csv:
            with open(tofile, 'a', newline='')as f:
                k.append(j[0] + "/" + j[1] + "/")
                f_csv = csv.writer(f)
                f_csv.writerow(k)
                k = []
    # duplicateDrop(tofile)


def get_FileSize(filePath):
    fp = open(filePath, "a")
    fsize = os.path.getsize(filePath)
    fsize = fsize / float(1000000)
    fp.close()
    return round(fsize, 2)

# get_FileSize("data/dependencies/dependencies1.csv")

# mergeCsv("data/wrongGA.csv", "data/error/wrongGA.csv")
# readCsvFromNrow("data/11.csv",5)
# duplicateDrop("data/3.csv")
#
# keepNrows("data/3-3.csv",39)
# # delete_empty_rows("data/2.csv")
#
# file1 = "data/3-2.csv"
# file2 = "data/3-1.csv"
# file3 = "data/3-3.csv"
# delRepeat(file1, file2, file3)

# parafile = "data/group*.csv"
# resultfile = "data/group.csv"
# mergeCsv(parafile, resultfile)
# duplicateDrop("data/group.csv")

# divideCsv(resultfile,resultfile)
# if __name__ == '__main__':
#     begin = time.time()
#     # csv_list = glob.glob("data/divide3/*.csv")
#     # for i in csv_list:
#     #     divideCsv(i,i)
#     splitByLineCount('data/divide3/3.csv', 1000)  # ????????????csv????????????1000???
#     end = time.time()
#     print('time is %d seconds ' % (end - begin))
# print(len(pd.read_csv("data/5.csv").index))
# print(pd.read_csv("data/5.csv"))

# csv_list = glob.glob("MDG_data/*.csv")  # ????????????????????????csv?????????
# print(u'?????????%s???CSV??????' % len(csv_list))
# print(u'????????????............')
# for i in csv_list:  # ??????????????????????????????csv??????
#     fr = open(i, 'rb').read()
#     with open("MDG_data/MDG_data.csv", 'ab') as f:  # ??????????????????result.csv
#         f.write(fr)


# delete_empty_rows("MDG_data/result3.csv")
# duplicateDrop("MDG_data/result3.csv")
# delete_empty_rows("MDG_data/result3-2-4.csv")
# duplicateDrop("MDG_data/result3-2-4.csv")
# delete_empty_rows("MDG_data/result4.csv")
# duplicateDrop("MDG_data/result4.csv")