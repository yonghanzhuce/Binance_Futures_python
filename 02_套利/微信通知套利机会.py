# 扫描数字货币市场是否有期现套利机会，如果有则通过微信通知
import time

class WechatNotifier():
    def __init__(self):
        self.corpid = "xxxxxxxxxxxxxxxxxxxx"
        self.corpsecret = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        self.agentid = "xxxxxxxxxxxxxxxxxxxx"
        self.touser = "xxxxxxxxxxxxxxxxxxxx"

    def send(self, content):
        url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=%s&corpsecret=%s" % (self.corpid, self.corpsecret)
        r = requests.get(url)
        access_token = r.json()['access_token']
        url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s" % access_token
        data = {
            "touser": self.touser,
            "msgtype": "text",
            "agentid": self.agentid,
            "text": {
                "content": content
            },
            "safe": 0
        }
        r = requests.post(url, json=data)
        print(r.text)

class ArbitrageInfoNotifier():
    def __init__(self):
        self.market_client = MarketClient()
        self.trade_client = TradeClient()
        self.notifier = WechatNotifier()
        self.symbols = [
            ('btc', 'this_week'),
            ('btc', 'next_week'),
            ('btc', 'quarter'),
            ('eth', 'this_week'),
            ('eth', 'next_week'),
            ('eth', 'quarter'),
            ('bch', 'this_week'),
            ('bch', 'next_week'),
            ('bch', 'quarter'),
            ('ltc', 'this_week'),
            ('ltc', 'next_week'),
            ('ltc', 'quarter'),
            ('etc', 'this_week'),
            ('etc', 'next_week'),
            ('etc', 'quarter'),
            ('eos', 'this_week'),
            ('eos', 'next_week'),
            ('eos', 'quarter'),
        ]
        self.contract_size = 10
        self.spread_threshold = 0.005
        self.leverage = 20
        self.margin_mode = "cross"
        self.spread_ratio = 0.05
        self.spread_ratio_threshold = 0.01
        self.spread_ratio_max = 0.05

    def run(self):
        while True:
            try:
                for symbol, contract_type in self.symbols:
                    # 获取现货的买一价和卖一价
                    price = self.market_client.get_ticker(symbol=symbol)
                    ask_price = float(price.ask_price)
                    bid_price = float(price.bid_price)
                    # 获取期货合约的买一价和卖一价
                    contract = self.market_client.get_contract(symbol=symbol, contract_type=contract_type)
                    contract_ask_price = float(contract.ask_price)
                    contract_bid_price = float(contract.bid_price)
                    # 计算价格差
                    spread = contract_ask_price - bid_price
                    # 如果价格差大于阈值
                    if spread > self.spread_threshold:
                        # 计算数量
                        amount = int(self.leverage * self.contract_size / ask_price)
                        # 发送通知
                        self.notifier.send(
                            "币安交易所数字货币期限套利机会",
                            "币种: %s, 合约类型: %s, 现货买一价: %s, 期货买一价: %s, 价格差: %s" % (symbol, contract_type, bid_price, contract_ask_price, spread)
                        )
                        # 下单
                        self.trade_client.create_order(
                            symbol=symbol,
                            contract_type=contract_type,
                            price=ask_price,
                            amount=amount,
                            lever_rate=self.leverage,
                            direction='buy',
                            offset='open',
                            margin_mode=self.margin_mode
                        )
                        self.trade_client.create_order(
                            symbol=symbol,
                            price=bid_price,
                            amount=amount,
                            direction='sell',
                            offset='open',
                            margin_mode=self.margin_mode
                        )
                    # 如果价格差小于阈值
                    elif spread < -self.spread_threshold:
                        # 计算数量
                        amount = int(self.leverage * self.contract_size / bid_price)
                        # 发送通知
                        self.notifier.send(
                            "币安交易所数字货币期限套利机会",
                            "币种: %s, 合约类型: %s, 现货卖一价: %s, 期货卖一价: %s, 价格差: %s" % (symbol, contract_type, ask_price, contract_bid_price, spread)
                        )
                        # 下单
                        self.trade_client.create_order(
                            symbol=symbol,
                            contract_type=contract_type,
                            price=bid_price,
                            amount=amount,
                            lever_rate=self.leverage,
                            direction='sell',
                            offset='open',
                            margin_mode=self.margin_mode
                        )
                        self.trade_client.create_order(
                            symbol=symbol,
                            price=ask_price,
                            amount=amount,
                            direction='buy',
                            offset='open',
                            margin_mode=self.margin_mode
                        )
                    # 如果价格差在阈值之间
                    else:
                        pass
            except Exception as e:
                self.notifier.send("数字货币期限套利机会", "发生异常: %s" % e)
            time.sleep(1)

if __name__ == '__main__':
    ArbitrageInfoNotifier().run()
