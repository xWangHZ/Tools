import re
import time
import smtplib
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from email.mime.text import MIMEText

driver = webdriver.Chrome()
# 浏览器


def login(content):
    url = "https://xui.ptlogin2.qq.com/cgi-bin/xlogin?appid=1600000931&pt_no_auth=1&daid=536&link_target=blank&target=self&hide_close_icon=1&style=20&low_login_enable=0&low_login_foreced=1&low_login_hour=720&hide_border=1&s_url=https%3A%2F%2Fdocs.qq.com%2Ftim%2Fdocs%2Fcomponents%2FBindQQ.html%3Ftype%3Dlogin&pt_isdocs=0"
    # 登录界面
    driver.get(url)
    time.sleep(1)
    driver.find_elements_by_id("switcher_plogin")[0].click()  # 单击账号密码登录
    driver.find_elements_by_id("u")[0].send_keys("")  # 输入账号
    driver.find_elements_by_id("p")[0].send_keys("")  # 输入密码
    driver.find_elements_by_id("login_button")[0].click()  # 单击登录
    time.sleep(2)
    localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    content = content + localtime + " 登录成功\n"
    print(content)
    return content


def gettable(content, flag):
    ch = 'E'
    while True:
        url = ""+ch+""
        driver.get(url)
        time.sleep(3)
        html = driver.page_source
        month_day = re.findall(r'<div class="cell-input" id="alloy-simple-text-editor" contenteditable="true" tabindex="1" style="white-space: pre-wrap; pointer-events: auto;">(.*?)<br class="extra">',html, re.S)
        timeday = str(month_day[0]).split('/')
        localtime = time.localtime(time.time())
        month = int(localtime[1])
        day = int(localtime[2])
        if int(timeday[0]) == month:
            if int(timeday[1]) == day:
                content = content + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " 已查找到日期\n"
                break
            else:
                ch = chr(int(ord(ch))+5)
        else:
            ch = chr(int(ord(ch)) + 5)
    if flag == 1:
        url = "" + ch + ""
        content = setvalue(url, 1, content)
        ch = chr(int(ord(ch)) + 2)

        url = "" + ch + ""
        content = setvalue(url, 2, content)
        ch = chr(int(ord(ch)) + 1)

        url = "" + ch + ""
        content = setvalue(url, 2, content)

        localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        content = content + localtime + " 上午体温已填完\n"
        print(content)
        return content
    elif flag == 2:

        ch = chr(int(ord(ch)) + 1)
        url = "" + ch + ""
        content = setvalue(url, 1, content)

        localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        content = content + localtime + " 下午体温已填完\n"
        print(content)
        return content


def setvalue(url, flag, content):
    driver.get(url)
    if flag == 1:
        time.sleep(2)
        elemt = driver.find_elements_by_id("alloy-simple-text-editor")[0]
        time.sleep(1)
        elemt.click()   # 单击文本框
        time.sleep(1)
        elemt.send_keys("36.5")    # 输入数据
        time.sleep(1)
        elemt.send_keys(Keys.BACK_SPACE)
        elemt.send_keys(Keys.BACK_SPACE)
        elemt.send_keys(Keys.BACK_SPACE)
        elemt.send_keys(Keys.BACK_SPACE)    # 退格
        time.sleep(1)
        elemt.send_keys("36.5")  # 输入数据
        time.sleep(3)
        elemt.send_keys(Keys.ENTER)     # 回车
        time.sleep(3)
        localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        content = content + localtime + " 已填写体温\n"
        print(content)
        return content
    elif flag == 2:
        time.sleep(2)
        elemt = driver.find_elements_by_id("alloy-simple-text-editor")[0]
        time.sleep(1)
        elemt.click()  # 单击文本框
        time.sleep(3)
        elemt.send_keys("无")  # 输入数据
        time.sleep(2)
        driver.find_element_by_id('alloy-simple-text-editor').click()
        elemt.send_keys(Keys.BACK_SPACE)
        time.sleep(2)
        elemt.send_keys("无")  # 输入数据
        time.sleep(3)
        elemt.send_keys(Keys.ENTER)
        time.sleep(3)
        localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        content = content + localtime + " 已填写流动\n"
        print(content)
        return content

def getemail(content):
    msg_from = ''  # 发送方邮箱
    passwd = ''  # 填入发送方邮箱的授权码
    msg_to = ''  # 收件人邮箱
    localtime = time.localtime(time.time())
    month = localtime[1]
    day = localtime[2]
    subject = str(month)+"月"+str(day)+"日体温"  # 主题

    msg = MIMEText(content) # 内容
    msg['Subject'] = subject
    msg['From'] = msg_from
    msg['To'] = msg_to
    try:
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 邮件服务器及端口号
        s.login(msg_from, passwd)
        s.sendmail(msg_from, msg_to, msg.as_string())
        print("发送成功")
        f = True
    except:
        print("发送失败")
        f = False
    finally:
        s.quit()
        return f


if __name__ == '__main__':
    content = ""
    while True:
        localtime = time.localtime(time.time())
        hour = int(localtime[3])
        minu = int(localtime[4])
        # 上午时间
        if hour == 14:
            if minu == 46:
                content = login(content)
                content = gettable(content, 1)
                f = getemail(content)
                driver.close()
                print(f)
                if f:
                    time.sleep(60)  # 休息一分钟防止多次填写
        # 下午时间
        if hour == 14:
            if minu == 4:
                content = login(content)
                content = gettable(content, 2)
                f = getemail(content)
                driver.close()
                print(f)
                if f:
                    time.sleep(60) # 休息一分钟防止多次填写