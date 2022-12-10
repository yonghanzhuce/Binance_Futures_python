# Path: 套利/期现套利/数字货币期限套利_全市场_多线程.py
# 扫描币安市场的数字货币期货合约和现货价格，看是否存在期现套利机会，需要考虑深度，手续费，杠杆，保证金模式等因素，如果有套利机会，自动下单。
# 期现套利策略：
# 期货合约的买一价和现货合约的卖一价之差大于0.5%时，买入期货合约，卖出现货合约
# 期货合约的卖一价和现货合约的买一价之差小于0.5%时，不做任何操作
import time
import threading
from huobi.client.market import MarketClient
from huobi.client.trade import TradeClient
from huobi.constant import *
from huobi.utils import *

class Arbitrager(threading.Thread):
    def __init__(self, symbol, contract_type, contract_size, spread_threshold, leverage, margin_mode):
        super(Arbitrager, self).__init__()
        self.symbol = symbol
        self.contract_type = contract_type
        self.contract_size = contract_size
        self.spread_threshold = spread_threshold
        self.leverage = leverage
        self.margin_mode = margin_mode
        self.market_client = MarketClient()
        self.trade_client = TradeClient()

    def run(self):
        while True:
            try:
                # 获取现货的买一价和卖一价
                price = self.market_client.get_ticker(symbol=self.symbol)
                ask_price = float(price['askPrice'])
                bid_price = float(price['bidPrice'])
                # 获取期货合约的买一价和卖一价
                contract = self.market_client.get_contract(symbol=self.symbol, contract_type=self.contract_type)
                contract_ask_price = float(contract['ask_price'])
                contract_bid_price = float(contract['bid_price'])
                # 计算价格差
                spread = contract_ask_price - bid_price
                # 如果价格差大于阈值
                if spread > self.spread_threshold:
                    # 计算数量
                    amount = int(self.leverage * self.contract_size / ask_price)
                    # 下单
                    self.trade_client.create_order(
                        symbol=self.symbol,
                        contract_type=self.contract_type,
                        price=ask_price,
                        amount=amount,
                        lever_rate=self.leverage,
                        direction='buy',
                        offset='open',
                        margin_mode=self.margin_mode
                    )
                    self.trade_client.create_order(
                        symbol=self.symbol,
                        price=bid_price,
                        amount=amount,
                        direction='sell',
                        offset='open',
                        margin_mode=self.margin_mode
                    )
                    print("套利机会: %s %s %s %s %s %s" % (self.symbol, self.contract_type, ask_price, bid_price, amount, spread))
                # 如果价格差小于阈值
                elif spread < -self.spread_threshold:
                    # 计算数量
                    amount = int(self.leverage * self.contract_size / bid_price)
                    # 下单
                    self.trade_client.create_order(
                        symbol=self.symbol,
                        contract_type=self.contract_type,
                        price=bid_price,
                        amount=amount,
                        lever_rate=self.leverage,
                        direction='sell',
                        offset='open',
                        margin_mode=self.margin_mode
                    )
                    self.trade_client.create_order(
                        symbol=self.symbol,
                        price=ask_price,
                        amount=amount,
                        direction='buy',
                        offset='open',
                        margin_mode=self.margin_mode
                    )
                    print("套利机会: %s %s %s %s %s %s" % (self.symbol, self.contract_type, ask_price, bid_price, amount, spread))
                # 如果价格差在阈值范围内
                else:
                    pass
            except Exception as e:
                print(e)
                pass
            time.sleep(1)

if __name__ == '__main__':
    # 币种列表
    symbols = [
        'btcusdt',
        'ethusdt',
        'ltcusdt',
        'bchusdt',
        'eosusdt',
        'xrpusdt',
        'etcusdt',
        'bsvusdt',
        'trxusdt',
        'htusdt',
        'linkusdt',
        'dotusdt',
        'atomusdt',
        'etcusdt',
        'ontusdt',
        'iostusdt',
        'zecusdt',
        'dashusdt',
        'omgusdt',
        'zilusdt',
        'zrxusdt',
        'thetausdt',
        'aionusdt',
        'batusdt',
        'neousdt',
        'qtumusdt',
        'elausdt',
        'iotausdt',
        'nasusdt',
        'aeusdt',
        'xemusdt',
        'sntusdt',
        'kncusdt',
        'storjusdt',
        'mdsusdt',
        'arnusdt',
        'gntusdt',
        'ruffusdt',
        'manausdt',
        'rdnusdt',
        'rcnusdt',
        'pptusdt',
        'waxusdt',
        'dtausdt',
        'elfusdt',
        'mithusdt',
        'mcousdt',
        'nasusdt',
    ]
    # 合约类型
    contract_type = ContractType.CW
    # 合约大小
    contract_size = 10
    # 价格差阈值
    spread_threshold = 0.5
    # 杠杆倍数
    leverage = 10
    # 保证金模式
    margin_mode = MarginMode.CROSSED
    # 创建套利机器人
    for symbol in symbols:
        Arbitrager(symbol, contract_type, contract_size, spread_threshold, leverage, margin_mode).start()
        