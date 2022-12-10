# 写一个策略，扫描币安市场是否有三角套利机会，如果有，就下单
# 三角套利的逻辑是：假设有三个交易对，A/B、B/C、C/A，那么就可以通过A/B、B/C、C/A三个交易对，实现A/C的套利
import pandas as pd
import time
class Arbitrager():
    def __init__(self, exchange):
        self.exchange = exchange
        self.exchange.load_markets()

    def get_common_base_list(self, market_a, market_b):
        """
        获取两个交易对的共同计价货币列表
        :param market_a:
        :param market_b:
        :return:
        """
        market_a_info = self.exchange.markets[market_a]
        market_b_info = self.exchange.markets[market_b]

        market_a_base = market_a_info['base']
        market_b_base = market_b_info['base']

        market_a_quote = market_a_info['quote']
        market_b_quote = market_b_info['quote']

        common_base_list = []
        if market_a_base == market_b_base:
            common_base_list.append(market_a_base)
        elif market_a_base == market_b_quote:
            common_base_list.append(market_a_base)
        elif market_a_quote == market_b_base:
            common_base_list.append(market_a_quote)
        elif market_a_quote == market_b_quote:
            common_base_list.append(market_a_quote)

        return common_base_list

    def get_arbitrage(self, market_a, market_b):
        """
        获取三角套利机会
        :param market_a:
        :param market_b:
        :return:
        """
        # == Step.1 获取交易对
        # 获取交易对列表
        symbols = self.exchange.symbols

        # 过滤出两个交易对的交易对列表
        market_a_symbols = [symbol for symbol in symbols if symbol.startswith(market_a)]
        market_b_symbols = [symbol for symbol in symbols if symbol.startswith(market_b)]

        # 获取两个交易对的共同计价货币列表
        common_base_list = self.get_common_base_list(market_a, market_b)

        # == Step.2 获取价格
        # 获取所有交易对的价格
        tickers = self.exchange.fetch_tickers()

        # 获取所有交易对的价格，保存到DataFrame中
        price_list = []
        for symbol in symbols:
            price = tickers[symbol]['close']
            price_list.append([symbol, price])

        price_pd = pd.DataFrame(price_list, columns=['symbol', 'price'])

        # == Step.3 执行套利步
        # 遍历两个交易对的交易对列表
        for market_a_symbol in market_a_symbols:
            for market_b_symbol in market_b_symbols:
                # 获取两个交易对的共同计价货币
                market_a_base = market_a_symbol.split('/')[0]
                market_b_base = market_b_symbol.split('/')[0]

                # 如果两个交易对的共同计价货币不在共同计价货币列表中，就跳过
                if market_a_base not in common_base_list or market_b_base not in common_base_list:
                    continue

                # 获取三个交易对的价格
                market_a_price = price_pd[price_pd['symbol'] == market_a_symbol]['price'].values[0]
                market_b_price = price_pd[price_pd['symbol'] == market_b_symbol]['price'].values[0]

                # 计算两个交易对的价格比例
                market_a_b_price_ratio = market_a_price / market_b_price

                # 获取两个交易对的共同计价货币
                market_a_quote = market_a_symbol.split('/')[1]
                market_b_quote = market_b_symbol.split('/')[1]

                # 获取三个交易对的名称
                market_a_b_symbol = market_a_quote + '/' + market_b_quote
                market_b_a_symbol = market_b_quote + '/' + market_a_quote

                # 获取三个交易对的价格
                market_a_b_price = price_pd[price_pd['symbol'] == market_a_b_symbol]['price'].values[0]
                market_b_a_price = price_pd[price_pd['symbol'] == market_b_a_symbol]['price'].values[0]

                # 计算三个交易对的价格比例
                market_a_b_a_price_ratio = market_a_b_price / market_b_a_price

                # 计算套利比例
                arbitrage_ratio = market_a_b_price_ratio / market_a_b_a_price_ratio

                # 如果套利比例大于1，就说明存在套利机会
                if arbitrage_ratio > 1:
                    print('存在套利机会：')
                    print('交易对：', market_a_symbol, market_b_symbol, market_a_b_symbol)
                    print('价格：', market_a_price, market_b_price, market_a_b_price)
                    print('比例：', market_a_b_price_ratio, market_a_b_a_price_ratio)
                    print('套利比例：', arbitrage_ratio)
    def run(self):
        """
        运行
        :return:
        """
        while True:
            self.get_arbitrage('BTC', 'ETH')
            time.sleep(1)


    