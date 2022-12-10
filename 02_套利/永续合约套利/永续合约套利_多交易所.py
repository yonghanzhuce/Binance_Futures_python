# 写一个币安的BTC_USDT和BTC_USDT_SWAP套利策略
import time
class Arbitrager():
    def __init__(self):
        # 初始化一些参数
        self.binance_symbol = "BTCUSDT"
        self.binance_client = Client()
        self.binance_order_id = []
        self.binance_order_status = []
        self.binance_order_price = []
        self.binance_order_amount = []
        self.binance_order_side = []
        self.okex_symbol = "BTC-USDT-SWAP"
        self.okex_client = OKEXClient()
        self.okex_order_id = []
        self.okex_order_status = []
        self.okex_order_price = []
        self.okex_order_amount = []
        self.okex_order_side = []

    def get_data(self):
        # 获取币安的行情数据
        self.binance_ticker = self.binance_client.get_ticker(symbol=self.binance_symbol)
        # 获取币安的深度数据
        self.binance_depth = self.binance_client.get_depth(symbol=self.binance_symbol)
        # 获取OKEX的行情数据
        self.okex_ticker = self.okex_client.get_ticker(symbol=self.okex_symbol)
        # 获取OKEX的深度数据
        self.okex_depth = self.okex_client.get_depth(symbol=self.okex_symbol)
    def check_order(self):
        # 检查是否有未成交的订单
        for order_id in self.binance_order_id:
            order = self.binance_client.get_order(symbol=self.binance_symbol, orderId=order_id)
            if order['status'] == 'FILLED':
                self.binance_order_status.append(order['status'])
            elif order['status'] == 'NEW':
                self.binance_order_status.append(order['status'])
            else:
                self.binance_order_status.append("CANCELLED")
        for order_id in self.okex_order_id:
            order = self.okex_client.get_order(symbol=self.okex_symbol, orderId=order_id)
            if order['status'] == 'FILLED':
                self.okex_order_status.append(order['status'])
            elif order['status'] == 'NEW':
                self.okex_order_status.append(order['status'])
            else:
                self.okex_order_status.append("CANCELLED")
    def check_arbitrage(self):
        # 检查是否有套利机会
        # 检查币安的买一价和OKEX的卖一价
        if float(self.binance_ticker['bidPrice']) > float(self.okex_ticker['askPrice']):
            # 买币安的卖OKEX的
            self.binance_order_side.append("BUY")
            self.okex_order_side.append("SELL")
            # 买的价格是币安的买一价
            self.binance_order_price.append(float(self.binance_ticker['bidPrice']))
            # 卖的价格是OKEX的卖一价
            self.okex_order_price.append(float(self.okex_ticker['askPrice']))
            # 买的数量是币安的深度中卖一价的数量
            self.binance_order_amount.append(float(self.binance_depth['asks'][0][1]))
            # 卖的数量是OKEX的深度中买一价的数量
            self.okex_order_amount.append(float(self.okex_depth['bids'][0][1]))
            # 买的数量和卖的数量取最小值
            amount = min(self.binance_order_amount[-1], self.okex_order_amount[-1])
            # 下单
            self.binance_order_id.append(self.binance_client.create_order(symbol=self.binance_symbol, side="BUY", type="MARKET", quantity=amount))
            self.okex_order_id.append(self.okex_client.create_order(symbol=self.okex_symbol, side="SELL", type="MARKET", quantity=amount))
        # 检查OKEX的买一价和币安的卖一价
        elif float(self.okex_ticker['bidPrice']) > float(self.binance_ticker['askPrice']):
            # 买OKEX的卖币安的
            self.binance_order_side.append("SELL")
            self.okex_order_side.append("BUY")
            # 买的价格是OKEX的买一价
            self.okex_order_price.append(float(self.okex_ticker['bidPrice']))
            # 卖的价格是币安的卖一价
            self.binance_order_price.append(float(self.binance_ticker['askPrice']))
            #
            self.okex_order_amount.append(float(self.okex_depth['bids'][0][1]))
            self.binance_order_amount.append(float(self.binance_depth['asks'][0][1]))
            amount = min(self.okex_order_amount[-1], self.binance_order_amount[-1])
            self.okex_order_id.append(self.okex_client.create_order(symbol=self.okex_symbol, side="BUY", type="MARKET", quantity=amount))
            self.binance_order_id.append(self.binance_client.create_order(symbol=self.binance_symbol, side="SELL", type="MARKET", quantity=amount))
        else:
            pass
    def run(self):
        while True:
            # 从币安和OKEX获取数据
            self.get_data()
            # 检查是否有未成交的订单
            self.check_order()
            # 检查是否有套利机会
            self.check_arbitrage()
            # 每隔1秒执行一次
            time.sleep(1)
if __name__ == '__main__':
    arbitrager = Arbitrager()
    arbitrager.run()
    