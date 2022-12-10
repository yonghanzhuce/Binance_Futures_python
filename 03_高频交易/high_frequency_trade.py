# 扫描币安交易所的所有币种，看是否有三角套利的机会
def triangular_arbitrage():
    # 获取所有交易对
    exchange_info = client.get_exchange_info()
    symbols = exchange_info['symbols']
    # 获取所有交易对的深度
    for symbol in symbols:
        symbol_name = symbol['symbol']
        depth = client.get_order_book(symbol=symbol_name)
        bids = depth['bids']
        asks = depth['asks']
        # 获取买一卖一的价格
        bid_price = float(bids[0][0])
        ask_price = float(asks[0][0])
        # 计算买一卖一的价差
        spread = ask_price - bid_price
        # 价差小于0.0001时，打印出来
        if spread < 0.0001:
            print(symbol_name, spread)
# 交易对的深度
def depth():
    depth = client.get_order_book(symbol='BNBBTC')
    print(depth)
# 最近成交
def trades():
    trades = client.get_recent_trades(symbol='BNBBTC')
    print(trades)
# 最近成交(归集)
def agg_trades():
    agg_trades = client.aggregate_trade_iter(symbol='BNBBTC', start_str='30 minutes ago UTC')
    for trade in agg_trades:
        print(trade)
# K线数据
def klines():
    klines = client.get_historical_klines("BNBBTC", Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")
    print(klines)
# 24小时价格变动情况
def ticker_24hr():
    ticker_24hr = client.get_ticker(symbol='BNBBTC')
    print(ticker_24hr)
# 最新价格
def ticker_price():
    ticker_price = client.get_all_tickers()
    print(ticker_price)
# 最新成交
def ticker_book():
    ticker_book = client.get_order_book(symbol='BNBBTC')
    print(ticker_book)
# 账户信息
def account():
    account = client.get_account()
    print(account)
# 账户交易列表
def my_trades():
    my_trades = client.get_my_trades(symbol='BNBBTC')
    print(my_trades)
# 下单
def order():
    order = client.create_test_order(
        symbol='BNBBTC',
        side=Client.SIDE_BUY,
        type=Client.ORDER_TYPE_LIMIT,
        timeInForce=Client.TIME_IN_FORCE_GTC,
        quantity=100,
        price='0.00001')
    print(order)
# 撤单
def cancel_order():
    order = client.cancel_order(
        symbol='BNBBTC',
        orderId=1)
    print(order)
# 查询订单
def query_order():
    order = client.get_order(
        symbol='BNBBTC',
        orderId=1)
    print(order)
    
