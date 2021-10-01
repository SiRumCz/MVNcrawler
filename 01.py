from getWeb import getWebContent
from getVersionDetail import getLastVersionDetail, getComDep
from getVersionDetail import getVersionDetail, getGroupId

mvn_url = "https://mvnrepository.com/artifact"
groupId = "edu.uci.ics"
artifactId = "crawler4j"
url = mvn_url + "/" + groupId + "/" + artifactId + "/"

# content = getWebContent("https://mvnrepository.com/artifact/com.dimafeng/testcontainers-scala-localstack")
content = getWebContent(mvn_url + "/" + groupId + "/" + artifactId + "/")

print(type(content))
# print(getGroupId(content))

print(getVersionDetail(content))

# result = getLastVersionDetail(content)
# for it in result:
#     print(it.group("href"))
#     print(it.group("version"))
#     print(it.group("usages"))

print(getComDep(getWebContent("https://mvnrepository.com/artifact/edu.uci.ics/crawler4j/4.4.0")))
