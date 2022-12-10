# 监控李大霄的微博，如果说了外资抄底，则将内容发送到微信
from threading import Timer
import requests
from bs4 import BeautifulSoup

def send_wechat(text):
    # 通过企业微信机器人发送消息
    url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxxxxxxxxxxxxxxxx'
    data = {
        "msgtype": "text",
        "text": {
            "content": text
        }
    }
    requests.post(url, json=data)

def monitor_weibo():
    # 读取微博消息
    url = 'https://s.weibo.com/weibo?q=%E6%9D%8E%E5%A4%A7%E9%9C%84&Refer=STopic_history'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    tweets = soup.find_all('p', class_='txt')
    # 检查是否有数字货币的相关信息
    for tweet in tweets:
        print(tweet.text)
        if '外资' in tweet.text and '抄底' in tweet.text:
            # 发送微信
            send_wechat(tweet.text)
            break
    # 每隔10分钟检查一次
    Timer(60, monitor_weibo).start()
