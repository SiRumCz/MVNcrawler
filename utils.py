import csv
import glob
import random
import os
import pandas as pd
import time

user_agent_list = [
    # Chrome
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


# 将大的csv文件拆分多个小的csv文件

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


# def splitByLineCount(filename, count):
#     fin = open(filename, encoding="utf-8")
#     try:
#         buf = []
#         sub = 1
#         for line in fin:
#             buf.append(line)
#             if len(buf) == count:
#                 sub = mkSubFile(buf, filename, sub)
#                 buf = []
#         if len(buf) != 0:
#             sub = mkSubFile(buf, filename, sub)
#     finally:
#         fin.close()


# 合并csv
def mergeCsv(paraFile, resultName):
    csv_list = glob.glob(paraFile)  # 查看同文件夹下的csv文件数
    print(u'共发现%s个CSV文件' % len(csv_list))
    print(u'正在处理............')
    for i in csv_list:  # 循环读取同文件夹下的csv文件
        fr = open(i, 'rb').read()
        with open(resultName, 'ab') as f:  # 将结果保存为result.csv
            f.write(fr)
    print(u'合并完毕！')


# 拆分csv只留第一列
def divideCsv(file, toFile):
    data = pd.read_csv(file, header=None)
    data.columns = ["A", "B"]
    data = data['A'].to_frame()
    data.to_csv(toFile, index=False, header=False)


# csv去重保留第一个
def duplicateDrop(file):
    data = pd.read_csv(file, header=None)
    data.drop_duplicates(subset=None, keep="first", inplace=True)
    data.to_csv(file, index=False, header=False)


# 删除空行
def delete_empty_rows(file_path):
    data = pd.read_csv(file_path, header=None)
    data.dropna(how="all", inplace=True)
    data.to_csv(file_path, index=False, header=False)


# 删除两个csv的重复项放到第三个文件
def delRepeat(file1, file2, file3):
    df1 = pd.read_csv(file1, header=None)
    df2 = pd.read_csv(file2, header=None)
    # print(df2)
    frames = [df1, df2]
    # print(frames)
    data = pd.concat(frames, sort=False).reset_index(drop=True)
    data.drop_duplicates(keep=False, inplace=True)
    data.to_csv(file3, index=False, header=False)


# csv保留前N行
def keepNrows(file, n):
    data = pd.read_csv(file, header=None, nrows=n)
    data.to_csv(file, index=False, header=False)


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
#     splitByLineCount('data/divide3/3.csv', 1000)  # 每个小的csv文件存放1000条
#     end = time.time()
#     print('time is %d seconds ' % (end - begin))
# print(len(pd.read_csv("data/5.csv").index))
# print(pd.read_csv("data/5.csv"))

# csv_list = glob.glob("data/*group.csv")  # 查看同文件夹下的csv文件数
# print(u'共发现%s个CSV文件' % len(csv_list))
# print(u'正在处理............')
# for i in csv_list:  # 循环读取同文件夹下的csv文件
#     fr = open(i, 'rb').read()
#     with open("data/result1.csv", 'ab') as f:  # 将结果保存为result.csv
#         f.write(fr)