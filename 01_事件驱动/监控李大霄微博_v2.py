# 通过微博API，监控李大霄最新的微博消息，如果说了外资抄底，则将内容发送到微信
import time
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
    # 读取李大霄微博
    url = 'https://m.weibo.cn/api/container/getIndex?containerid=1005051829086393'
    r = requests.get(url)
    weibo = r.json()['data']['cards'][0]['mblog']['text']
    # 检查是否有外资抄底
    if '外资抄底' in weibo and '外资' in weibo:
        # 发送微信
        send_wechat(weibo)

if __name__ == '__main__':
    while True:
        monitor_weibo()
        time.sleep(600)
