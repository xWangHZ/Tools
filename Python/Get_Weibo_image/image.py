import requests
import os

name = 672
for page in range(50, 100):
    # 页数
    url = "https://m.weibo.cn/api/container/getIndex?containerid=2304131549575922&page="+str(page)
    # 爬取的URL
    response = requests.get(url)
    json = response.json()
    # 以 Json 对象返回
    data = json['data']
    # 解析字段 data
    cards = data['cards']
    # 解析字段 cards
    for card in cards:
        my_blog = card['mblog']
        for key in my_blog:
            if key == "pics":
                pics = my_blog['pics']
                for pics_index in pics:
                    large = pics_index['large']
                    print(large['url'])
                    img_url = large['url']
                    img = requests.get(img_url)
                    byte = img.content
                    with open('image/'+str(name)+'.jpg','wb') as f:
                        f.write(byte)
                    name+=1
                    print(name)
