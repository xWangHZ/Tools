import requests
import re

url = "https://newapp.jxnoa.cn/services/RemedialTeaching/Video.aspx?cid=4215&vid="
Header = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36"}


for i in range(750, 2000):
    urls = url+str(i)
    html = requests.get(urls, headers=Header).text
    # print(html)
    video = re.findall(r'<video src="(.*?)" poster.*?>', html, re.S)
    if len(video) > 0:
        print(video[0])
