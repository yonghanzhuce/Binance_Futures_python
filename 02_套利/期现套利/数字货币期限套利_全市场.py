# 扫描币安市场的数字货币期货合约和现货价格，看是否存在期现套利机会，如果有，就进行套利
# 期货合约的买一价和现货合约的卖一价之差大于0.5%时，买入期货合约，卖出现货合约
# 期货合约的卖一价和现货合约的买一价之差大于0.5%时，卖出期货合约，买入现货合约
# 期货合约的买一价和现货合约的卖一价之差小于0.5%时，不做任何操作
import time
from huobi.client.market import MarketClient
from huobi.client.trade import TradeClient
from huobi.constant import *
from huobi.utils import *

class Arbitrager():
    def __init__(self):
        # 初始化一些参数
        self.symbols = ["BTCUSDT", "ETHUSDT"]
        self.client = Client()
        self.contract_types = ["quarter", "this_week", "next_week"]
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
                for symbol in self.symbols:
                    # 获取现货的买一价和卖一价
                    price = self.client.get_ticker(symbol=symbol)
                    ask_price = float(price['askPrice'])
                    bid_price = float(price['bidPrice'])
                    # 获取期货合约的买一价和卖一价
                    for contract_type in self.contract_types:
                        contract = self.client.get_contract(symbol=symbol, contract_type=contract_type)
                        contract_ask_price = float(contract['ask_price'])
                        contract_bid_price = float(contract['bid_price'])
                        # 计算价格差
                        spread = contract_ask_price - bid_price
                        # 如果价格差大于阈值
                        if spread > self.spread_threshold:
                            # 计算数量
                            amount = int(self.leverage * self.contract_size / ask_price)
                            # 下单
                            self.client.create_order(
                                symbol=symbol,
                                contract_type=contract_type,
                                price=ask_price,
                                amount=amount,
                                lever_rate=self.leverage,
                                direction='buy',
                                offset='open',
                                margin_mode=self.margin_mode
                            )
                            self.client.create_order(
                                symbol=symbol,
                                price=bid_price,
                                amount=amount,
                                direction='sell',
                                offset='open',
                                margin_mode=self.margin_mode
                            )
                            print("套利机会: %s %s %s %s %s %s" % (symbol, contract_type, ask_price, bid_price, amount, spread))
                        # 如果价格差小于阈值
                        elif spread < -self.spread_threshold:
                            # 计算数量
                            amount = int(self.leverage * self.contract_size / bid_price)
                            # 下单
                            self.client.create_order(
                                symbol=symbol,
                                contract_type=contract_type,
                                price=bid_price,
                                amount=amount,
                                lever_rate=self.leverage,
                                direction='sell',
                                offset='open',
                                margin_mode=self.margin_mode
                            )
                            self.client.create_order(
                                symbol=symbol,
                                price=ask_price,
                                amount=amount,
                                direction='buy',
                                offset='open',
                                margin_mode=self.margin_mode
                            )
                            print("套利机会: %s %s %s %s %s %s" % (symbol, contract_type, ask_price, bid_price, amount, spread))
                        # 如果价格差在阈值范围内
                        else:
                            pass
            except Exception as e:
                print(e)
                pass
            time.sleep(1)

if __name__ == '__main__':
    arbitrager = Arbitrager()
    arbitrager.run()