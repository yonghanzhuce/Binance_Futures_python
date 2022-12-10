# 写一个币安的BTC_USDT和BTC_USDT_SWAP资金费率套利策略
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
        self.okex_funding_rate = []
    def get_data(self):
        # 获取币安的行情数据
        self.binance_ticker = self.binance_client.get_ticker(symbol=self.binance_symbol)
        # 获取币安的深度数据
        self.binance_depth = self.binance_client.get_depth(symbol=self.binance_symbol)
        # 获取OKEX的行情数据
        self.okex_ticker = self.okex_client.get_ticker(symbol=self.okex_symbol)
        # 获取OKEX的深度数据
        self.okex_depth = self.okex_client.get_depth(symbol=self.okex_symbol)
        # 获取OKEX的资金费率
        self.okex_funding_rate.append(self.okex_client.get_funding_rate(symbol=self.okex_symbol))
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
    def arbitrage(self):
        # 套利逻辑
        if self.okex_funding_rate[-1] > 0:
            # 如果OKEX的资金费率为正，说明OKEX的合约价格高于现货价格
            # 那么我们就在币安买入现货，然后在OKEX卖出合约
            # 买入现货
            self.binance_order_side.append("BUY")
            self.binance_order_price.append(float(self.binance_ticker['bidPrice']))
            self.binance_order_amount.append(1)
            self.binance_order_id.append(self.binance_client.create_order(symbol=self.binance_symbol, side="BUY", type="MARKET", quantity=1))
            # 卖出合约
            self.okex_order_side.append("SELL")
            self.okex_order_price.append(float(self.okex_ticker['askPrice']))
            self.okex_order_amount.append(1)
            self.okex_order_id.append(self.okex_client.create_order(symbol=self.okex_symbol, side="SELL", type="MARKET", quantity=1))
        else:
            # 如果OKEX的资金费率为负，说明OKEX的合约价格低于现货价格
            # 那么我们就在币安卖出现货，然后在OKEX买入合约
            # 卖出现货
            self.binance_order_side.append("SELL")
            self.binance_order_price.append(float(self.binance_ticker['askPrice']))
            self.binance_order_amount.append(1)
            self.binance_order_id.append(self.binance_client.create_order(symbol=self.binance_symbol, side="SELL", type="MARKET", quantity=1))
            # 买入合约
            self.okex_order_side.append("BUY")
            self.okex_order_price.append(float(self.okex_ticker['bidPrice']))
            self.okex_order_amount.append(1)
            self.okex_order_id.append(self.okex_client.create_order(symbol=self.okex_symbol, side="BUY", type="MARKET", quantity=1))
    def run(self):
        # 主循环
        while True:
            self.get_data()
            self.check_order()
            self.arbitrage()
            time.sleep(1)
if __name__ == '__main__':
    arbitrage = Arbitrager()
    arbitrage.run()
