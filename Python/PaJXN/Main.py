import requests
import re
import os

cookie = ""
# 使用自己的cookie
header = {'Cookie': cookie}
# url = "https://newapp.jxnoa.cn/basevideo/networkvideo.ashx?videoid=5360"
# html = requests.get(url, headers=header)
# html = html.text
# print(html)
for i in range(5360, 5461):
    url = "https://newapp.jxnoa.cn/basevideo/networkvideo.ashx?videoid="+str(i)
    # id = 5450需要单独下载
    if not (i <= 5453 and i >= 5446) and i != 5443:
        q = requests.get(url, headers=header)
        html = q.text
        if q.status_code == 200:
            name = re.findall(r'"标题":"(.*?)"', str(html), re.S)
            fe = re.findall(r'"学科":(.*?),', str(html), re.S)
            vurl = re.findall(r'"视频":"(.*?)"', str(html), re.S)
            if str(fe[0]) == "20" or str(fe[0]) == "10":
                path = "video/"+str(fe[0])
                #需要创建video文件夹
                if not os.path.exists(path):
                    os.mkdir(path)
                r = requests.get(str(vurl[0]))
                print(name[0] + " " + url)
                with open(path+"/"+str(name[0])+".mp4", "wb") as f:
                    for chunk in r.iter_content(chunk_size=1024 * 1024):
                        if chunk:
                            f.write(chunk)
