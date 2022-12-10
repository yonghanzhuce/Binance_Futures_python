import requests
def send_slack_message(text):
    # 发送slack消息
    url = 'https://hooks.slack.com/services/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'
    data = {'text': text}
    requests.post(url, json=data)