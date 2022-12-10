# 写一个币安数字货币的期现套利程序，可以自动检测套利机会并下单
# 期货合约：BTC-USD-200925
# 现货合约：BTC/USDT
# 期货合约的买一价和现货合约的卖一价之差大于0.5%时，买入期货合约，卖出现货合约
# 期货合约的卖一价和现货合约的买一价之差大于0.5%时，卖出期货合约，买入现货合约
# 期货合约的买一价和现货合约的卖一价之差小于0.5%时，不做任何操作
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
        self.okex_symbol = "BTC-USD-200925"
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
        # 检查币安的买一价和OKEX的卖一价之差
        if float(self.binance_ticker['bidPrice']) - float(self.okex_ticker['askPrice']) > 0.005:
            # 买入币安，卖出OKEX
            self.binance_order_side.append("BUY")
            self.okex_order_side.append("SELL")
            self.binance_order_price.append(float(self.binance_ticker['bidPrice']))
            self.okex_order_price.append(float(self.okex_ticker['askPrice']))
            self.binance_order_amount.append(1)
            self.okex_order_amount.append(1)
        # 检查OKEX的买一价和币安的卖一价之差
        elif float(self.okex_ticker['bidPrice']) - float(self.binance_ticker['askPrice']) > 0.005:
            # 买入OKEX，卖出币安
            self.binance_order_side.append("SELL")
            self.okex_order_side.append("BUY")
            self.binance_order_price.append(float(self.binance_ticker['askPrice']))
            self.okex_order_price.append(float(self.okex_ticker['bidPrice']))
            self.binance_order_amount.append(1)
            self.okex_order_amount.append(1)
        else:
            # 不做任何操作
            pass
    def send_order(self):
        # 发送订单
        for i in range(len(self.binance_order_side)):
            if self.binance_order_side[i] == "BUY":
                order = self.binance_client.create_order(symbol=self.binance_symbol, side="BUY", type="MARKET", quantity=1)
                self.binance_order_id.append(order['orderId'])
            elif self.binance_order_side[i] == "SELL":
                order = self.binance_client.create_order(symbol=self.binance_symbol, side="SELL", type="MARKET", quantity=1)
                self.binance_order_id.append(order['orderId'])
        for i in range(len(self.okex_order_side)):
            if self.okex_order_side[i] == "BUY":
                order = self.okex_client.create_order(symbol=self.okex_symbol, side="BUY", type="MARKET", quantity=1)
                self.okex_order_id.append(order['orderId'])
            elif self.okex_order_side[i] == "SELL":
                order = self.okex_client.create_order(symbol=self.okex_symbol, side="SELL", type="MARKET", quantity=1)
                self.okex_order_id.append(order['orderId'])
    def run(self):
        while True:
            self.get_data()
            self.check_order()
            self.check_arbitrage()
            self.send_order()
            time.sleep(1)
if __name__ == '__main__':
    arbitrage = Arbitrager()
    arbitrage.run()

