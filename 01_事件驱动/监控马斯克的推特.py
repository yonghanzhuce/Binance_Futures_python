# 通过推特API监控马斯克最近10分钟的推特消息，如果有数字货币的相关信息，则将内容发送到微信
from threading import Timer
import requests
from bs4 import BeautifulSoup
import tweepy
import os


def send_slack_message(text):
    # 发送slack消息
    url = 'https://hooks.slack.com/services/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'
    data = {'text': text}
    requests.post(url, json=data)

def monitor_musk_twitter():
    # 监控马斯克最近10分钟的推特消息，如果有数字货币的相关信息，则将内容发送到微信
    # 获取推特信息
    auth = tweepy.OAuthHandler("yPnrgrI7UNl9cFisDAD0kVozR", "YHEPqGpiDgUflvdzSxAkHDAxUsGPJOHCArt7oDG5upzr9hDheZ")
    auth.set_access_token('1531797238338375680-UGY7C7hkisUGmAHLM8lm1NPTQWmN2j', 'nxzjf5U4k8NN257kE2MjhEyXz02TeoTL4eIm18beO594I')
    api = tweepy.API(auth)
    # user = api.get_user(screen_name='elonmusk')
    tweets = api.user_timeline(screen_name = "elonmusk",count=10)
    # 判断推特内容是否是数字货币相关的
    for tweet in tweets:
        if 'bitcoin' in tweet.text or 'crypto' in tweet.text:
            send_slack_message(tweet.text)
    # 每隔5分钟执行一次
    # Timer(300, monitor_musk_twitter).start()

if __name__ == '__main__':
    monitor_musk_twitter()
    
