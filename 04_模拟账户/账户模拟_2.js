// 模拟证券交易所账户，提供下单，卖出等服务，最后计算账户的收益
class SimulatedAccount {
    constructor() {
        this._cash = 0;
        this._positions = {};
    }
    setCash(cash) {
        this._cash = cash;
    }
    getCash() {
        return this._cash;
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
        this._positions[symbol] = (this._positions[symbol] || 0) + shares;
    }
    sell(symbol, price, shares) {
        const position = this._positions[symbol];
        if (!position) {
            throw "No position";
        }
        if (position < shares) {
            throw "Not enough position";
        }
        this._positions[symbol] = position - shares;
        const cost = price * shares;
        this._cash += cost;
    }
    getValue(price) {
        let value = this._cash;
        for (let symbol in this._positions) {
            const shares = this._positions[symbol];
            value += shares * price;
        }
        return value;
    }
}

// test
const account = new SimulatedAccount();
account.setCash(1000);
account.order("AAPL",1000, 1);
account.sell("AAPL",1100, 1);
console.log(account.getValue());

