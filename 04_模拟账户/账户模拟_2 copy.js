class SimulatedAccount {
    constructor() {
        this._cash = 0;
        this._positions = {};
        this._orders = [];
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
        this._orders.push({
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
        this._positions[symbol] = position - shares;
        const cost = price * shares;
        this._cash += cost;
        this._orders.push({
            symbol,
            price,
            shares,
            type: "sell"
        });
    }
    cancelOrder(order) {
        const index = this._orders.indexOf(order);
        if (index === -1) {
            throw "Order not found";
        }
        this._orders.splice(index, 1);
        if (order.type === "buy") {
            this._cash += order.price * order.shares;
            this._positions[order.symbol] -= order.shares;
        } else {
            this._cash -= order.price * order.shares;
            this._positions[order.symbol] += order.shares;
        }
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