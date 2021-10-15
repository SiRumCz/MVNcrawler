import csv
import os
import time
import pandas as pd

from getWeb import getWebContent
from getHref import getFirstHref, getNextHref, writeNextHrefToCsvE, badGetFirstHref, \
    badWriteNextHrefToCsvE, goodWriteNextHrefToCsvE
from LibLink import getLibLink, divideGroupArtifact
from utils import duplicateDrop, delete_empty_rows

print("start:" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

repo_url = "https://repo1.maven.org/maven2/"
group1_list = badGetFirstHref(getWebContent(repo_url))
print(group1_list)
ls = ["1"]
try:
    with open('data/0.csv', 'w', newline='')as f:
        f_csv = csv.writer(f)
        for i in range(len(group1_list)):
            ls[0] = group1_list[i]
            # print(ls[0])
            f_csv.writerow(ls)
except UnicodeEncodeError:
    pass

fileFinal = "data/group3.csv"
lst = []
lstFinal = []
file2 = ""
emptyFile = "data/empty.csv"
for i in range(0, 0):
    fileName = "data/" + str(i) + ".csv"
    file2 = "data/" + str(i + 1) + ".csv"
    print(fileName + time.strftime('  %Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    if os.stat(fileName).st_size == 0:
        os.remove(fileName)
        break
    else:
        duplicateDrop(fileName)
        delete_empty_rows(fileName)
        with open(fileName)as f:
            g1_csv = csv.reader(f)
            for j in g1_csv:
                # print(j)
                badWriteNextHrefToCsvE(repo_url, j, lst, lstFinal)
                # g1_csv.drop(i)
                if len(lst) >= 1000:
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
                if len(lstFinal) >= 1000:
                    print("lstFinal=", end='')
                    print(lstFinal)
                    try:
                        with open(fileFinal, 'a', newline='')as f:
                            f_csv = csv.writer(f)
                            f_csv.writerows(lstFinal)
                        lstFinal = []
                    except UnicodeEncodeError:
                        for k in lstFinal:
                            try:
                                with open(fileFinal, 'a', newline='')as f:
                                    f_csv = csv.writer(f)
                                    f_csv.writerow(k)

                            except UnicodeEncodeError:
                                print(k)
                                lstFinal[lstFinal.index(k)] = ''
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
    print("the last lstFinal=", end='')
    print(lstFinal)
    try:
        with open(fileFinal, 'a', newline='')as f:
            f_csv = csv.writer(f)
            f_csv.writerows(lstFinal)
        lstFinal = []
    except UnicodeEncodeError:
        for k in lstFinal:
            try:
                with open(fileFinal, 'a', newline='')as f:
                    f_csv = csv.writer(f)
                    f_csv.writerow(k)

            except UnicodeEncodeError:
                print(k)
                lstFinal[lstFinal.index(k)] = ''
        lstFinal = []
    print("end:" + time.strftime('  %Y-%m-%d %H:%M:%S', time.localtime(time.time())))

print("2 end:" + time.strftime('  %Y-%m-%d %H:%M:%S', time.localtime(time.time())))

for i in range(6, 100):
    fileName = "data/" + str(i) + ".csv"
    file2 = "data/" + str(i + 1) + ".csv"
    print(fileName + time.strftime('  %Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    if os.stat(fileName).st_size == 0:
        os.remove(fileName)
        break
    else:
        duplicateDrop(fileName)
        delete_empty_rows(fileName)
        with open(fileName)as f:
            g1_csv = csv.reader(f)
            for j in g1_csv:
                # print(j)
                goodWriteNextHrefToCsvE(repo_url, j, lst, lstFinal)
                # g1_csv.drop(i)
                if len(lst) >= 1000:
                    print("lst=", end='')
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
                        pass
                else:
                    pass
                if len(lstFinal) >= 1000:
                    print("lstFinal=", end='')
                    print(lstFinal)
                    try:
                        with open(fileFinal, 'a', newline='')as f:
                            f_csv = csv.writer(f)
                            f_csv.writerows(lstFinal)
                        lstFinal = []
                    except UnicodeEncodeError:
                        for k in lstFinal:
                            try:
                                with open(fileFinal, 'a', newline='')as f:
                                    f_csv = csv.writer(f)
                                    f_csv.writerow(k)

                            except UnicodeEncodeError:
                                print(k)
                                lstFinal[lstFinal.index(k)] = ''
                        lstFinal = []
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
        for k in lst:
            try:
                with open(file2, 'a', newline='')as f:
                    f_csv = csv.writer(f)
                    f_csv.writerow(k)

            except UnicodeEncodeError:
                print(k)
                lst[lst.index(k)] = ''
        lst = []
    print("the last lstFinal=", end='')
    print(lstFinal)
    try:
        with open(fileFinal, 'a', newline='')as f:
            f_csv = csv.writer(f)
            f_csv.writerows(lstFinal)
        lstFinal = []
    except UnicodeEncodeError:
        for k in lstFinal:
            try:
                with open(fileFinal, 'a', newline='')as f:
                    f_csv = csv.writer(f)
                    f_csv.writerow(k)

            except UnicodeEncodeError:
                print(k)
                lstFinal[lstFinal.index(k)] = ''
        lstFinal = []
    print("end:" + time.strftime('  %Y-%m-%d %H:%M:%S', time.localtime(time.time())))
