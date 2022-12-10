# 监控推特消息，如果发生比特币利好，则发送slack消息
from threading import Timer
import requests
from bs4 import BeautifulSoup

def monitor_twitter():
    # 读取推特消息
    url = 'https://twitter.com/search?q=bitcoin&src=typd'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    tweets = soup.find_all('p', class_='tweet-text')
    # 检查是否有比特币利好
    for tweet in tweets:
        if 'bitcoin' in tweet.text.lower():
            # 发送微信
            # send_wechat(tweet.text)
            break
    # 每隔10分钟检查一次
    Timer(2, monitor_twitter).start()


def send_slack_message(text):
    # 发送slack消息
    url = 'https://hooks.slack.com/services/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'
    data = {'text': text}
    requests.post(url, json=data)
