import requests
from getWeb import getWebContent
from getHref import getFirstHref, getNextHref
from LibLink import getLibLink, easyGetLibLink

repo_url = "https://repo1.maven.org/maven2/cn/"

group1_list = getFirstHref(getWebContent(repo_url))
print(group1_list)
print(len(group1_list))
flag = 1
g_list = []
while flag == 1:
    if len(group1_list) == 0:
        break
    else:
        group1_list, g_list = getNextHref(repo_url, group1_list, g_list)

# print(group1_list)
print(g_list)
print(len(g_list))

# print(easyGetLibLink(g_list))

