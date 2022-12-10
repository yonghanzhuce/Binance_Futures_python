# 使用airtest，写一个监控微信群消息的脚本，当有新消息时，判断新消息中是否包含关键字，如果包含关键字则发送slack消息提醒

from airtest.core.api import *

class WechatMessageMonitor():
    def __init__(self):
        self.slack = Slack()
        self.wechat = Wechat()
        self.wechat.start()
        self.slack.start()
        self.wechat.login()
        self.wechat.enter_chatroom('测试群')
        self.wechat.set_monitor(self.monitor)

    def monitor(self, msg):
        if '关键字' in msg:
            self.slack.send_msg(msg)
        else:
            print('没有关键字')

    def run(self):
        self.wechat.run()

class Wechat():
    def __init__(self):
        self.wechat = connect_device('Android:///')
        self.wechat.start_app('com.tencent.mm')
        self.monitor = None

    def start(self):
        self.wechat.start_app('com.tencent.mm')

    def login(self):
        if exists(Template(r"tpl1611157071985.png", record_pos=(0.0, 0.0), resolution=(1080, 2340))):
            touch(Template(r"tpl1611157071985.png", record_pos=(0.0, 0.0), resolution=(1080, 2340)))
    
    def enter_chatroom(self, chatroom_name):
        touch(Template(r"tpl1611157154427.png", record_pos=(-0.001, -0.001), resolution=(1080, 2340)))
    
    def set_monitor(self, monitor):
        self.monitor = monitor
    
    def run(self):
        while True:
            if exists(Template(r"tpl1611157224205.png", record_pos=(0.0, 0.0), resolution=(1080, 2340))):
                touch(Template(r"tpl1611157224205.png", record_pos=(0.0, 0.0), resolution=(1080, 2340)))
                sleep(1)
                msg = self.wechat.get_text(Template(r"tpl1611157263371.png", record_pos=(0.0, 0.0), resolution=(1080, 2340)))
                self.monitor(msg)
            time.sleep(1)

class Slack():
    def __init__(self):
        pass

    def start(self):
        pass

    def login(self):
        pass
    
    def send_msg(self, msg):
        pass
    

if __name__ == '__main__':
    WechatMessageMonitor().run()

    
    