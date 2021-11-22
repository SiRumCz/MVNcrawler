import _thread
import csv
import os
import threading
import time

from getWeb import getWebContent
from getHref import getFirstHref, getNextHref,  writeNextHrefToCsvE, recheckEmpty
from LibLink import getLibLink, divideGroupArtifact

repo_url = "https://repo1.maven.org/maven2/"


class myThread(threading.Thread):
    def __init__(self, threadID, repo_url, file):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.repo_url = repo_url
        self.file = file

    def run(self):
        print("开始线程：" + self.name)
        recheckEmpty(self.repo_url, self.file)
        print("退出线程：" + self.name)


# file = "data/" + str(i) + "-1.csv"
# 创建新线程

thread1 = myThread(1, repo_url, "data/2-1.csv")
thread2 = myThread(2, repo_url, "data/3-1.csv")
# thread3 = myThread(3, repo_url, 200, 300, "data/divide3/result/group3.csv", "data/divide3/result/4_3.csv")
# thread4 = myThread(4, repo_url, 300, 400, "data/divide3/result/group4.csv", "data/divide3/result/4_4.csv")
# thread5 = myThread(5, repo_url, 400, 500, "data/divide3/result/group5.csv", "data/divide3/result/4_5.csv")

# 开启新线程
thread1.start()
thread2.start()
# thread3.start()
# thread4.start()


thread1.join()
thread2.join()
# thread3.join()
# thread4.join()
print("退出主线程")
# print("start:" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
# thread1 = myThread(1, repo_url, 1, 25, "data/divide3/result/group3.csv", "data/divide3/result/4_1.csv")
# thread2 = myThread(2, repo_url, 25, 50, "data/divide3/result/group2.csv", "data/divide3/result/4_2.csv")
# thread1.start()
# thread2.start()
# thread1.join()
# thread2.join()
# print(time.strftime("50 done" + '%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
#
# thread1 = myThread(1, repo_url, 50, 75, "data/divide3/result/group3.csv", "data/divide3/result/4_3.csv")
# thread2 = myThread(2, repo_url, 75, 100, "data/divide3/result/group4.csv", "data/divide3/result/4_4.csv")
# thread1.start()
# thread2.start()
# thread1.join()
# thread2.join()
# print(time.strftime("100 done" + '%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
#
# thread1 = myThread(1, repo_url, 100, 125, "data/divide3/result/group5.csv", "data/divide3/result/4_5.csv")
# thread2 = myThread(2, repo_url, 125, 150, "data/divide3/result/group6.csv", "data/divide3/result/4_6.csv")
# thread1.start()
# thread2.start()
# thread1.join()
# thread2.join()
# print(time.strftime("150 done" + '%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
#
# thread1 = myThread(1, repo_url, 150, 175, "data/divide3/result/group7.csv", "data/divide3/result/4_7.csv")
# thread2 = myThread(2, repo_url, 175, 200, "data/divide3/result/group8.csv", "data/divide3/result/4_8.csv")
# thread1.start()
# thread2.start()
# thread1.join()
# thread2.join()
# print(time.strftime("200 done" + '%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
#
# thread1 = myThread(1, repo_url, 200, 225, "data/divide3/result/group9.csv", "data/divide3/result/4_9.csv")
# thread2 = myThread(2, repo_url, 225, 250, "data/divide3/result/group10.csv", "data/divide3/result/4_10.csv")
# thread1.start()
# thread2.start()
# thread1.join()
# thread2.join()
# print(time.strftime("250 done" + '%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

# thread1 = myThread(1, repo_url, 1, 2, "data/divide3/result/group3.csv", "data/divide3/result/4_1.csv")
# thread1.start()
# thread1.join()
