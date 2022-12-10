# 实现模拟股票交易的虚拟盘小工具（巴菲特模拟器）
class Simulator:
    def __init__(self, cash):
        self.cash = cash
        self.stocks = {}
        self.history = []
    def buy(self, stock, price, amount):
        if self.cash >= price*amount:
            self.cash -= price*amount
            if stock in self.stocks:
                self.stocks[stock] += amount
            else:
                self.stocks[stock] = amount
            self.history.append((stock, price, amount))
    def sell(self, stock, price, amount):
        if stock in self.stocks and self.stocks[stock] >= amount:
            self.cash += price*amount
            self.stocks[stock] -= amount
            self.history.append((stock, price, -amount))
    def __str__(self):
        return 'cash: %s
        