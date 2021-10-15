import csv
import os

from getWeb import getWebContent
from getHref import getFirstHref, getNextHref, writeNextHrefToCsv
from LibLink import getLibLink, divideGroupArtifact

repo_url = "https://repo1.maven.org/maven2/"

group1_list = getFirstHref(getWebContent(repo_url))
try:
    with open('data/0.csv', 'w', newline='')as f:
        f_csv = csv.writer(f)
        f_csv.writerows(group1_list)
except UnicodeEncodeError:
    pass

print(group1_list)
print(len(group1_list))

fileFinal = "data/group2.csv"

for i in range(0, 100):
    fileName = "data/" + str(i) + ".csv"
    file2 = "data/" + str(i + 1) + ".csv"
    if os.path.exists(fileName):
        with open(fileName)as f:
            g1_csv = csv.reader(f)
            for j in g1_csv:
                # print(j)
                writeNextHrefToCsv(repo_url, j, file2, fileFinal)
                # g1_csv.drop(i)
    else:
        break

# flag = 1
# g_list = []
# while flag == 1:
#     with open('g1.csv')as f:
#         g1_csv = csv.reader(f)
#         headers = next(g1_csv)
#         for i in g1_csv:
#             group1_list, g_list = getNextHref(repo_url, group1_list, g_list)
#
# print(g_list)
# print(len(g_list))


# flag = 1
# g_list = []
# while flag == 1:
#     if len(group1_list) == 0:
#         break
#     else:
#         group1_list, g_list = getNextHref(repo_url, group1_list, g_list)
#
# # print(group1_list)
# print(g_list)
# print(len(g_list))
#
# print(easyGetLibLink(g_list))
