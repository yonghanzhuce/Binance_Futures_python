# 写一个币安的BTC_USDT数字货币永续合约套利策略
import time
class Arbitrager():
    def __init__(self):
        # 初始化一些参数
        self.symbol = "BTCUSDT"
        self.client = Client()
        self.order_id = []
        self.order_status = []
        self.order_price = []
        self.order_amount = []
        self.order_side = []
    def run(self):
        # 从币安获取数据
        self.get_data()
        # 检查是否有未成交的订单
        self.check_order()
        # 检查是否有套利机会
        self.check_arbitrage()
    def get_data(self):
        # 获取币安的行情数据
        self.ticker = self.client.get_ticker(symbol=self.symbol)
        # 获取币安的深度数据
        self.depth = self.client.get_depth(symbol=self.symbol)
    def check_order(self):
        # 检查是否有未成交的订单
        for order_id in self.order_id:
            order = self.client.get_order(symbol=self.symbol, orderId=order_id)
            if order['status'] == 'FILLED':
                self.order_status.append(order['status'])
            elif order['status'] == 'NEW':
                self.order_status.append(order['status'])
            else:
                self.order_status.append("CANCELLED")
    def check_arbitrage(self):
        # 检查是否有套利机会
        # 买一价
        bid_price = float(self.ticker['bidPrice'])
        # 卖一价
        ask_price = float(self.ticker['askPrice'])
        # 买一价和卖一价之间的差价
        spread = ask_price - bid_price
        # 深度数据中最后一个价格
        last_price = float(self.depth['bids'][-1][0])
        # 买一价和深度数据中最后一个价格之间的差价
        bid_spread = bid_price - last_price
        # 获取深度数据中最后一个价格的挂单量
        bid_amount = float(self.depth['bids'][-1][1])
        # 深度数据中第一个价格
        first_price = float(self.depth['asks'][0][0])
        # 卖一价和深度数据中第一个价格之间的差价
        ask_spread = first_price - ask_price
        # 获取深度数据中第一个价格的挂单量
        ask_amount = float(self.depth['asks'][0][1])
        # 如果买一价和深度数据中最后一个价格之间的差价大于0.1
        if bid_spread > 0.1:
            # 以买一价买入
            self.buy(bid_price, bid_amount)
        # 如果深度数据中第一个价格和卖一价之间的差价大于0.1
        if ask_spread > 0.1:
            # 以卖一价卖出
            self.sell(ask_price, ask_amount)
        # 如果买一价和卖一价之间的差价大于0.1
        if spread > 0.1:
            # 以买一价买入
            self.buy(bid_price, bid_amount)
            # 以卖一价卖出
            self.sell(ask_price, ask_amount)
    def buy(self, price, amount):
        # 买入
        order = self.client.order_market_buy(symbol=self.symbol, quantity=amount)
        self.order_id.append(order['orderId'])
        self.order_price.append(price)
        self.order_amount.append(amount)
        self.order_side.append('BUY')
    def sell(self, price, amount):
        # 卖出
        order = self.client.order_market_sell(symbol=self.symbol, quantity=amount)
        self.order_id.append(order['orderId'])
        self.order_price.append(price)
        self.order_amount.append(amount)
        self.order_side.append('SELL')
# 主程序
if __name__ == '__main__':
    # 初始化策略
    strategy = Arbitrager()
    # 每隔1秒运行一次
    while True:
        strategy.run()
        time.sleep(1)
