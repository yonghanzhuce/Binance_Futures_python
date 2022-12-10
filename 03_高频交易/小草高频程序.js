/*backtest
start: 2021-11-30 00:00:00
end: 2022-12-06 00:00:00
period: 1d
basePeriod: 1h
*/

// fmz@a4e9361d1026bf44bdae34654a4a03b1

/*
就是我刚开始编写机器人的源代码，几乎没有改动，参数也是原来的参数。这个版本的程序有许多
需要改进的地方，但即使如此，它也当时表现除了惊人的盈利能力，在我本金不多时，不加杠杆平
均每天盈利在5%左右。当然无论从哪一方面，它都不适应今天的市场。
我同时也发了一篇文章在社区，大家可以看看。
by 小草
*/

//稍微改了一下，用了平台的容错函数_C(),和精度函数_N().
//取消全部订单

// 创建模拟仿真交易系统，包含待成交订单，已成交订单，持仓，资金，账户信息等
class SimulatedAccount {
    constructor() {
        this._cash = 0;
        this._freeze_cash = 0;
        this._positions = {};
        this._complete_orders = [];
        this._sent_orders = [];
    }
    getSentOrders() {
        return this._sent_orders;
    }
    getFreezeCash() {
        return this._freeze_cash;
    }
    setCash(cash) {
        this._cash = cash;
    }
    getCash() {
        return this._cash;
    }
    getTotalCash() {
        return this._cash + this._freeze_cash;
    }
    getPosition(symbol) {
        return this._positions[symbol] || 0;
    }
    setPosition(symbol, position) {
        this._positions[symbol] = position;
    }
    order(symbol, price, shares) {
        const cost = price * shares;
        if (this._cash < cost) {
            throw "Not enough cash";
        }
        this._cash -= cost;
        this._freeze_cash += cost;
    
        this._sent_orders.push({
            symbol,
            price,
            shares,
            type: "buy"
        });
    }
    sell(symbol, price, shares) {
        const position = this._positions[symbol];
        if (!position) {
            throw "No position";
        }
        if (position < shares) {
            throw "Not enough position";
        }
        this._sent_orders.push({
            symbol,
            price,
            shares,
            type: "sell"
        });
    }
    cancelAllSellTypeSentOrders() {
        this._sent_orders = this._sent_orders.filter(order => order.type !== "sell");
    }
    cancelAllBuyTypeSentOrders() {
        this._sent_orders = this._sent_orders.filter(order => order.type !== "buy");
        this._cash += this._freeze_cash;
        this._freeze_cash = 0;
    }
    getValue(prices) {
        let value = this._cash + this._freeze_cash;
        for (let symbol in this._positions) {
            const shares = this._positions[symbol];
            value += shares * prices[symbol].close;
        }
        return value;
    }

    simulatedTransaction(prices){
        for (let i = 0; i < this._sent_orders.length; i++) {
            const order = this._sent_orders[i];
            if (order.type === "buy") {
                if (order.price < prices[order.symbol].low) {
                    return;
                }

                Log("买入挂单成功交易。")
                Log("买入挂单价格：",order.price)
                Log("上个区间最低价",prices[order.symbol].low)
                Log("当前价格：", exchange.GetTicker().Last)
                const cost = order.price * order.shares;
                this._freeze_cash -= cost;
                this._positions[order.symbol] = (this._positions[order.symbol] || 0) + order.shares;
                this._sent_orders.splice(i, 1);
                i--;
            } else {
                if (order.price > prices[order.symbol].high) {
                    return;
                }
                Log("卖出挂单成功交易。")
                Log("卖出挂单价格：",order.price)
                Log("上个区间最高价",prices[order.symbol].high)
                Log("当前价格：", exchange.GetTicker().Last)
                const cost = order.price * order.shares;
                this._positions[order.symbol] -= order.shares;
                this._cash += cost;
                this._sent_orders.splice(i, 1);
                i--;
            }
            this._complete_orders.push(order);
        }
    }
}

var account = new SimulatedAccount();
account.setCash("1000000")

function CancelPendingOrders() {
    var orders = _C(exchange.GetOrders);
    for (var j = 0; j < orders.length; j++) {
          exchange.CancelOrder(orders[j].Id, orders[j]);}
}

//计算将要下单的价格
function GetPrice(Type,depth) {
    var amountBids=0;
    var amountAsks=0;
    //计算买价，获取累计深度达到预设的价格
    if(Type=="Buy"){
       for(var i=0;i<20;i++){
           amountBids+=depth.Bids[i].Amount;
           //floatamountbuy就是预设的累计买单深度
           if (amountBids>floatamountbuy){
               //稍微加0.01，使得订单排在前面
              return depth.Bids[i].Price+0.01;}
        }
    }
    //同理计算卖价
    if(Type=="Sell"){
       for(var j=0; j<20; j++){
    	   amountAsks+=depth.Asks[j].Amount;
            if (amountAsks>floatamountsell){
            return depth.Asks[j].Price-0.01;}
        }
    }
    //遍历了全部深度仍未满足需求，就返回一个价格，以免出现bug
    return depth.Asks[0].Price
}
 
function onTick() {
    var depth=_C(exchange.GetDepth);
    var buyPrice = GetPrice("Buy",depth);
    var sellPrice= GetPrice("Sell",depth);
    //买卖价差如果小于预设值diffprice，就会挂一个相对更深的价格
    if ((sellPrice - buyPrice) <= diffprice){
            buyPrice-=10;
            sellPrice+=10;}
    //把原有的单子全部撤销，实际上经常出现新的价格和已挂单价格相同的情况，此时不需要撤销
    account.cancelAllBuyTypeSentOrders();
    account.cancelAllSellTypeSentOrders();
    //获取账户信息，确定目前账户存在多少钱和多少币
    // var account=_C(exchange.GetAccount);
    //可买的比特币量
    // var amountBuy = _N((account.Balance / buyPrice-0.1),2); 
    var amountBuy = _N((account.getCash() / buyPrice-0.1),2); 
    //可卖的比特币量，注意到没有仓位的限制，有多少就买卖多少，因为我当时的钱很少
    // var amountSell = _N((account.Stocks),2);
    var amountSell = _N((account.getPosition("BTC_USDT")),2); 
    if (amountSell > 0.02) {
        // exchange.Sell(sellPrice,amountSell);}
        account.sell("BTC_USDT",sellPrice, amountSell);
        Log("Sell Order :", sellPrice,amountSell)
    }
    if (amountBuy > 0.02) {
        // exchange.Buy(buyPrice, amountBuy);
        account.order("BTC_USDT",buyPrice, amountBuy);
        Log("Buy Order :", buyPrice, amountBuy)

    }
    //休眠，进入下一轮循环
    Sleep(sleeptime);
}

function main() {
    var i = 0;
    while (true) {
        account.simulatedTransaction({"BTC_USDT": {low:exchange.GetTicker().Low, high:exchange.GetTicker().High, close:exchange.GetTicker().Last}})
        onTick();
        // 每1000次输出一次log
        if (i % 100 === 0) {
            i = 0
            Log("Account Cash :", account.getCash())
            Log("Account Posion :", account.getPosition("BTC_USDT"))
            Log("Account Value :", account.getValue({"BTC_USDT": {"close" : exchange.GetTicker().Last}}))
            Log("Last Price :", exchange.GetTicker().Last)
        }
    }
    i++;
}