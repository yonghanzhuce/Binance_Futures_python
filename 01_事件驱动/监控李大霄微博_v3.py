# 通过微博API，监控李大霄最近一年的微博消息，使用paddle的NLP情感分析模块，分析其每次发文对股市的乐观或悲观态度，然后通过matplotlib绘制出趋势图
# 如果说了外资抄底，则将内容发送到微信
import time
import requests
from bs4 import BeautifulSoup
import paddle
import paddle.nn.functional as F
import paddlenlp as ppnlp
import json
from paddlenlp import Taskflow

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
    sentiment_trend = []
    # 读取李大霄微博
    url = 'https://m.weibo.cn/api/container/getIndex?containerid=1005051829086393'
    r = requests.get(url)
    weibo = r.json()['data']['cards']
    # 检查是否有外资抄底
    for w in weibo:
        if '外资抄底' in w['mblog']['text'] and '外资' in w['mblog']['text']:
            # 发送微信
            send_wechat(w['mblog']['text'])
        # 分析情绪
        sentiment_trend.append(sentiment_analysis(w['mblog']['text'])[0]['score'])


    # 绘制趋势图
    draw_trend(sentiment_trend)

def draw_trend(sentiment_trend):
    # 绘制趋势图
    import matplotlib.pyplot as plt
    plt.plot(sentiment_trend)
    plt.show()

def sentiment_analysis(sentence):
    
    schema = '情感倾向[正向，负向]'
    few_ie = Taskflow("sentiment_analysis", schema=schema,model="skep_ernie_1.0_large_ch", batch_size=16)

    # result的格式[{'text': '这个电影真的很好看', 'label': 'positive', 'score': 0.9996919631958008}]
    result=few_ie(sentence)
    if result[0]['label'] == 'negative':
        result[0]['score'] = result[0]['score'] * -1

    return result

if __name__ == '__main__':
    while True:
        monitor_weibo()
        time.sleep(600)
