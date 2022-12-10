# 扫描币安市场的数字货币期货合约和现货价格，看是否存在期现套利机会，如果有，就进行套利
# 期货合约的买一价和现货合约的卖一价之差大于0.5%时，买入期货合约，卖出现货合约
# 期货合约的卖一价和现货合约的买一价之差大于0.5%时，卖出期货合约，买入现货合约
# 期货合约的买一价和现货合约的卖一价之差小于0.5%时，不做任何操作
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
        self.contract_type = "quarter"
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
        # 获取币安的期货行情数据
        self.contract_ticker = self.client.get_contract_ticker(symbol=self.symbol, contractType=self.contract_type)
        # 获取币安的期货深度数据
        self.contract_depth = self.client.get_contract_depth(symbol=self.symbol, contractType=self.contract_type)
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
        # 期货合约买一价
        contract_bid_price = float(self.contract_ticker['bidPrice'])
        # 期货合约卖一价
        contract_ask_price = float(self.contract_ticker['askPrice'])
        # 期货合约买一价和卖一价之间的差价
        contract_spread = contract_ask_price - contract_bid_price
        # 期货合约深度数据中最后一个价格
        contract_last_price = float(self.contract_depth['bids'][-1][0])
        # 期货合约深度数据中最后一个价格和卖一价之间的差价
        contract_last_spread = contract_ask_price - contract_last_price
        # 现货合约买一价
        spot_bid_price = float(self.ticker['bidPrice'])
        # 现货合约卖一价
        spot_ask_price = float(self.ticker['askPrice'])
        # 现货合约买一价和卖一价之间的差价
        spot_spread = spot_ask_price - spot_bid_price
        # 现货合约深度数据中最后一个价格
        spot_last_price = float(self.depth['bids'][-1][0])
        # 现货合约深度数据中最后一个价格和卖一价之间的差价
        spot_last_spread = spot_ask_price - spot_last_price
        # 期货合约买一价和现货合约卖一价之间的差价
        arbitrage_spread = contract_bid_price - spot_ask_price
        # 期货合约买一价和现货合约卖一价之间的差价占现货合约卖一价的比例
        arbitrage_spread_ratio = arbitrage_spread / spot_ask_price
        # 期货合约买一价和现货合约卖一价之间的差价占现货合约卖一价的比例大于0.5%时，买入期货合约，卖出现货合约
        if arbitrage_spread_ratio > 0.005:
            # 买入期货合约的数量
            contract_buy_amount = 10
            # 卖出现货合约的数量
            spot_sell_amount = contract_buy_amount * contract_bid_price / spot_ask_price
            # 买入期货合约
            contract_buy_order = self.client.create_order(symbol=self.symbol, side=Client.SIDE_BUY, type=Client.ORDER_TYPE_MARKET, quantity=contract_buy_amount, contractType=self.contract_type)
            # 卖出现货合约
            spot_sell_order = self.client.create_order(symbol=self.symbol, side=Client.SIDE_SELL, type=Client.ORDER_TYPE_MARKET, quantity=spot_sell_amount)
            # 记录订单信息
            self.order_id.append(contract_buy_order['orderId'])
            self.order_id.append(spot_sell_order['orderId'])
            self.order_price.append(contract_bid_price)
            self.order_price.append(spot_ask_price)
            self.order_amount.append(contract_buy_amount)
            self.order_amount.append(spot_sell_amount)
            self.order_side.append("BUY")
            self.order_side.append("SELL")

        # 如果现货合约卖一价和期货合约买一价之间的差价大于0，说明现货合约卖一价高于期货合约买一价，可以进行套利
        elif arbitrage_spread > 0:
            # 买入现货合约的数量
            spot_buy_amount = 10
            # 卖出期货合约的数量
            contract_sell_amount = spot_buy_amount * spot_bid_price / contract_ask_price
            # 买入现货合约
            spot_buy_order = self.client.create_order(symbol=self.symbol, side=Client.SIDE_BUY, type=Client.ORDER_TYPE_MARKET, quantity=spot_buy_amount)
            # 卖出期货合约
            contract_sell_order = self.client.create_order(symbol=self.symbol, side=Client.SIDE_SELL, type=Client.ORDER_TYPE_MARKET, quantity=contract_sell_amount, contractType=self.contract_type)
            # 记录订单信息
            self.order_id.append(spot_buy_order['orderId'])
            self.order_id.append(contract_sell_order['orderId'])
            self.order_price.append(spot_bid_price)
            self.order_price.append(contract_ask_price)
            self.order_amount.append(spot_buy_amount)
            self.order_amount.append(contract_sell_amount)
            self.order_side.append("BUY")
            self.order_side.append("SELL")
    def on_order_update(self, event):
        # 获取订单更新信息
        order = event.dict_['data']
        # 如果订单状态为FILLED，说明订单已经成交
        if order['status'] == 'FILLED':
            # 获取订单在订单列表中的索引
            index = self.order_id.index(order['orderId'])
            # 获取订单成交的价格
            price = self.order_price[index]
            # 获取订单成交的数量
            amount = self.order_amount[index]
            # 获取订单的方向
            side = self.order_side[index]
            # 如果订单方向为BUY，说明是买入订单，需要增加持仓数量
            if side == "BUY":
                self.position += amount
            # 如果订单方向为SELL，说明是卖出订单，需要减少持仓数量
            elif side == "SELL":
                self.position -= amount
            # 计算持仓均价
            self.avg_price = (self.avg_price * self.position + price * amount) / (self.position + amount)
            # 计算持仓盈亏
            self.pnl = (price - self.avg_price) * self.position
            # 记录持仓信息
            self.position_list.append(self.position)
            self.avg_price_list.append(self.avg_price)
            self.pnl_list.append(self.pnl)
            self.time_list.append(datetime.now())
            # 将订单从订单列表中删除
            self.order_id.pop(index)
            self.order_price.pop(index)
            self.order_amount.pop(index)
            self.order_side.pop(index)
    def on_stop(self):
        # 将持仓信息保存到csv文件中
        df = pd.DataFrame({'time': self.time_list, 'position': self.position_list, 'avg_price': self.avg_price_list, 'pnl': self.pnl_list})
        df.to_csv('position.csv', index=False)
    def run(self):
        # 运行策略
        self.strategy.run()
        # 将策略中的订单信息保存到csv文件中
        df = pd.DataFrame({'orderId': self.order_id, 'price': self.order_price, 'amount': self.order_amount, 'side': self.order_side})
        df.to_csv('order.csv', index=False)
    def load_data(self):
        # 从csv文件中加载策略中的订单信息
        df = pd.read_csv('order.csv')
        self.order_id = df['orderId'].tolist()
        self.order_price = df['price'].tolist()
        self.order_amount = df['amount'].tolist()
        self.order_side = df['side'].tolist()
        # 从csv文件中加载策略中的持仓信息
        df = pd.read_csv('position.csv')
        self.position_list = df['position'].tolist()
        self.avg_price_list = df['avg_price'].tolist()
        self.pnl_list = df['pnl'].tolist()
        self.time_list = df['time'].tolist()
        # 获取最新的持仓信息
        self.position = self.position_list[-1]
        self.avg_price = self.avg_price_list[-1]
        self.pnl = self.pnl_list[-1]
        self.time = self.time_list[-1]
if __name__ == '__main__':
    # 创建策略对象
    strategy = Strategy()
    # 运行策略
    strategy.run()
    # 将策略中的订单信息保存到csv文件中
    df = pd.DataFrame({'orderId': strategy.order_id, 'price': strategy.order_price, 'amount': strategy.order_amount, 'side': strategy.order_side})
    df.to_csv('order.csv', index=False)
    # 将策略中的持仓信息保存到csv文件中
    df = pd.DataFrame({'time': strategy.time_list, 'position': strategy.position_list, 'avg_price': strategy.avg_price_list, 'pnl': strategy.pnl_list})
    df.to_csv('position.csv', index=False)

