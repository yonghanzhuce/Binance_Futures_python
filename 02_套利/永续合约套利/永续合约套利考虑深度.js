// 写一个币安的BTC_USDT和BTC_USDT_SWAP永续合约资金费率套利策略, 需要根据深度数据来判断是否可以套利
class Arbitrager {
    constructor() {
        this._name = 'Arbitrager';
        this._version = '0.1.0';
        this._author = 'hank';
        this._description = 'Arbitrager';
        this._exchange = 'binance';
        this._symbol = 'BTC_USDT';
        this._symbol_swap = 'BTC_USDT_SWAP';
        this._interval = 1;
        this._last_price = 0;
        this._last_price_swap = 0;
        this._last_funding_rate = 0;
        this._last_funding_rate_swap = 0;
        this._last_funding_time = 0;
        this._last_funding_time_swap = 0;
        this._last_funding_rate_timestamp = 0;
        this._last_funding_rate_timestamp_swap = 0;
    }
    async onInit() {
        // 订阅永续合约的资金费率
        this.subscribeFundingRate(this._symbol_swap);
    }
    async onFundingRate(symbol, fundingRate, fundingTime) {
        if (symbol == this._symbol_swap) {
            this._last_funding_rate_swap = fundingRate;
            this._last_funding_time_swap = fundingTime;
            this._last_funding_rate_timestamp_swap = Date.now();
        }
    }
    async checkFundingRate(symbol) {
        if (symbol == this._symbol) {
            this._last_funding_rate = fundingRate;
            this._last_funding_time = fundingTime;
            this._last_funding_rate_timestamp = Date.now();
        }
    }
    async checkDepth(symbol) {
        if (symbol == this._symbol) {
            let depth = await this._exchange.getDepth(symbol);
            let asks = depth.asks;
            let bids = depth.bids;
            let ask_price = asks[0][0];
            let bid_price = bids[0][0];
            let ask_volume = asks[0][1];
            let bid_volume = bids[0][1];
            let diff = ask_price - bid_price;
            if (diff > 0.1) {
                // 买入永续合约，卖出币币合约
                this.buy(this._symbol_swap, ask_price, ask_volume);
                this.sell(this._symbol, bid_price, bid_volume);
            }
        }
    }
    
    async onTick(symbol, lastPrice, bidPrice, askPrice, volume, bidVolume, askVolume) {
        if (symbol == this._symbol) {
            this._last_price = lastPrice;
        } else if (symbol == this._symbol_swap) {
            this._last_price_swap = lastPrice;
        }
        if (this._last_funding_rate_timestamp_swap > 0) {
            // 两个合约的资金费率差值
            let diff = this._last_funding_rate_swap - this._last_funding_rate;
            // 两个合约的价格差值
            let diff_price = this._last_price_swap - this._last_price;
            // 两个合约的资金费率差值与价格差值的比值
            let ratio = diff / diff_price;
            // 两个合约的资金费率差值与价格差值的比值大于0.0001时，说明资金费率差值比较大，可以进行套利
            if (ratio > 0.0001) {
                // 买入永续合约，卖出币币合约
                this.buy(this._symbol_swap, this._last_price_swap, 0.001);
                this.sell(this._symbol, this._last_price, 0.001);
            }
        }
    }
    async subscribeFundingRate(symbol) {
        this._exchange.subscribeFundingRate(symbol);
    }
    async buy(symbol, price, amount) {
        this._exchange.buy(symbol, price, amount);
    }
    async sell(symbol, price, amount) {
        this._exchange.sell(symbol, price, amount);
    }

}
module.exports = Arbitrager;
