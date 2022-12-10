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
                const cost = order.price * order.shares;
                this._freeze_cash -= cost;
                this._positions[order.symbol] = (this._positions[order.symbol] || 0) + order.shares;
                this._sent_orders.splice(i, 1);
                i--;
            } else {
                if (order.price > prices[order.symbol].high) {
                    return;
                }
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

// test
const account = new SimulatedAccount();
account.setCash(100000);
account.order("000001", 10, 1000);
account.order("000002", 10, 1000);
console.log(account.getCash());
console.log(account.getPosition());
console.log(account.getFreezeCash());
console.log(account.getTotalCash());
console.log(account.getValue({"000001":{low:10,high:10,close:10},"000002":{low:10,high:10,close:10}}));
console.log(account.getSentOrders());

account.cancelAllBuyTypeSentOrders();
console.log(account.getCash());
console.log(account.getPosition());
console.log(account.getFreezeCash());
console.log(account.getTotalCash());
console.log(account.getValue({"000001":{low:10,high:10,close:10},"000002":{low:10,high:10,close:10}}));
console.log(account.getSentOrders());


account.order("000001", 10, 1000);
account.order("000002", 10, 1000);
account.simulatedTransaction({"000001":{low:10,high:10,close:10},"000002":{low:10,high:10,close:10}});
console.log(account.getCash());
console.log(account.getPosition());
console.log(account.getFreezeCash());
console.log(account.getTotalCash());
console.log(account.getValue({"000001":{low:10,high:10,close:10},"000002":{low:10,high:10,close:10}}));
console.log(account.getSentOrders());


account.sell("000001", 30, 1000);
account.sell("000002", 30, 1000);
account.simulatedTransaction({"000001":{low:30,high:30,close:30},"000002":{low:30,high:30,close:30}});
console.log(account.getCash());
console.log(account.getPosition());
console.log(account.getFreezeCash());
console.log(account.getTotalCash());
console.log(account.getValue({"000001":{low:30,high:30,close:30},"000002":{low:30,high:30,close:30}}));
console.log(account.getSentOrders());

