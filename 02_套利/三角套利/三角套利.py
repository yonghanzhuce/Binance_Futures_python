import pandas as pd
import time
import re
import requests
import warnings
warnings.filterwarnings("ignore")

pd.set_option('expand_frame_repr', False)


def main():
    """
        主函数
    """
    def split_symbol(symbol):

        replace_token = ["USDT", "BTC", "ETH", "BNB", "BUSD", "USDC", "TUSD", "PLN", "PAX", "XRP", "TRX", "NGN", "RUB",
                         "TRY", "EUR", "ZAR", "BKRW", "DRT", "GBP", "UAH", "IDR", "KRW", "AUD", "DAI", "BRL", "VAI",
                         "OGE", "UST", "DOT", "PLN"]
        for token in replace_token:
            if re.match(r'.*' + token + '$', symbol):
                symbol = symbol.replace(token, "-" + token)
                break
        return symbol



    # Defining Binance API URL
    url = "https://api.binance.com/api/v3/ticker/price"

    start = time.time()
    data = requests.get(url)
    data = data.json()

    price_pd = pd.DataFrame(data)
    print(f"{time.time() - start}")
    price_pd['symbol'] = price_pd['symbol'].apply(split_symbol)

    # == Step.1 选择两个交易市场 A, B
    market_a = 'BTC'
    market_b = 'ETH'
    # # == Step.1 END =================
    #
    # # == Step.2 找到所有同时以 A 和 B 都作为计价的货币
    # # 市场内的交易对
    # symbols = list(markets.keys())
    #
    # # 存放到DataFrame中
    # symbols_df = pd.DataFrame(data=symbols, columns=['symbol'])

    # 分割字符串得到 基础货币/计价货币

    base_quote_df = price_pd['symbol'].str.split(pat='-', expand=True)
    base_quote_df.columns = ['base', 'quote', 'other']

    # 过滤得到以 A, B 计价的计价货币
    base_a_list = base_quote_df[base_quote_df['quote'] == market_a]['base'].values.tolist()
    base_b_list = base_quote_df[base_quote_df['quote'] == market_b]['base'].values.tolist()

    # 获取相同的基础货币列表
    common_base_list = list(set(base_a_list).intersection(set(base_b_list)))
    print('{}和{}共有{}个相同的计价货币'.format(market_a, market_b, len(common_base_list)))
    print(common_base_list)
    # == Step.2 END =================

    # # == Step.3 执行套利步骤
    #
    # 结果保存到DataFrame中
    columns = ['Market A',
               'Market B',
               'Market C',
               'P1',
               'P2',
               'P3',
               'Profit(‰)']

    results_df = pd.DataFrame(columns=columns)

    # # 获取前一分钟的close价格
    # last_min = binance_exchange.milliseconds() - 60 * 1000  # 前一分钟
    #
    for base_coin in common_base_list:
        market_c = base_coin
        market_a2b_symbol = '{}-{}'.format(market_b, market_a)
        market_b2c_symbol = '{}-{}'.format(market_c, market_b)
        market_a2c_symbol = '{}-{}'.format(market_c, market_a)

        # 获取行情前一分钟的交易对价格
        p1 = price_pd[price_pd['symbol'] == market_a2b_symbol]['price'].values[0]
        p2 = price_pd[price_pd['symbol'] == market_b2c_symbol]['price'].values[0]
        p3 = price_pd[price_pd['symbol'] == market_a2c_symbol]['price'].values[0]
        p1 = float(p1)
        p2 = float(p2)
        p3 = float(p3)

        if p1 <= 0 or p2 <= 0 or p3 <= 0:
            continue

        # 计算利润
        profit = (p3 / p1 * p2 - 1) * 1000

        # # 利润大于0.1‰，则保存到结果中
        # if profit > 0.1:
        #     results_df.loc[len(results_df)] = [market_a,
        #                                        market_b,
        #                                        market_c,
        #                                        p1,
        #                                        p2,
        #                                        p3,
        #                                        profit]
        # # 价差
        # profit = (float(p3) / (float(p1) * float(p2) - 1) * 1000

        results_df = results_df.append({
            'Market A': market_a,
            'Market B': market_b,
            'Market C': market_c,
            'P1': p1,
            'P2': p2,
            'P3': p3,
            'Profit(‰)': profit
        }, ignore_index=True)

        # 显示信息
        # print(results_df.tail(1))

        # 防止超过rate limit
        # time.sleep(binance_exchange.rateLimit / 1000)
    # == Step.3 END =================

    results_df.to_csv('./tri_arbitrage_results.csv', index=None)

if __name__ == '__main__':
    main()
