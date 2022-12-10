# Path: 套利/期现套利/数字货币期限套利_全市场_多线程.py
# 扫描币安市场的数字货币期货合约和现货价格，看是否存在期现套利机会，如果有套利机会，自动下单。
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
                # 获取期货合约的买一价和卖一价
                contract_ticker = self.market_client.get_contract_ticker(self.symbol, self.contract_type)
                contract_bid_price = contract_ticker.bid[0].price
                contract_ask_price = contract_ticker.ask[0].price
                # 获取现货合约的买一价和卖一价
                spot_ticker = self.market_client.get_ticker(self.symbol)
                spot_bid_price = spot_ticker.bid
                spot_ask_price = spot_ticker.ask
                # 计算期现套利价差
                spread = (contract_bid_price - spot_ask_price) / spot_ask_price * 100
                # 如果期现套利价差大于阈值，买入期货合约，卖出现货合约
                if spread > self.spread_threshold:
                    # 获取账户余额
                    account_balance = self.trade_client.get_account_balance(self.symbol)
                    # 计算买入期货合约的数量
                    contract_buy_amount = account_balance.balance * self.leverage / contract_ask_price / self.contract_size
                    # 计算卖出现货合约的数量
                    spot_sell_amount = account_balance.balance * self.leverage / spot_bid_price
                    # 下单
                    self.trade_client.post_contract_order(symbol=self.symbol, contract_type=self.contract_type, contract_code=None, client_order_id=None, price=contract_ask_price, volume=contract_buy_amount, direction=OrderDirection.BUY, offset=Offset.OPEN, lever_rate=self.leverage, order_price_type=OrderPriceType.LIMIT, order_source=OrderSource.API, margin_mode=self.margin_mode)
                    self.trade_client.post_order(symbol=self.symbol, account_id=None, client_order_id=None, price=spot_bid_price, volume=spot_sell_amount, order_type=OrderType.SELL_LIMIT, source=OrderSource.API)
                    print('套利机会：', self.symbol, '买入期货合约', contract_buy_amount, '张，卖出现货合约', spot_sell_amount, '个')
                else:
                    print('套利机会：', self.symbol, '无')
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
        