// -------------------------------------------------------------------------------

// PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
// https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

// -------------------------------------------------------------------------------

namespace ccxt;

public partial class cex : Exchange
{
    public cex (object args = null): base(args) {}

    public async Task<object> publicGetCurrencyProfile (object parameters = null)
    {
        return await this.callAsync ("publicGetCurrencyProfile",parameters);
    }

    public async Task<object> publicGetCurrencyLimits (object parameters = null)
    {
        return await this.callAsync ("publicGetCurrencyLimits",parameters);
    }

    public async Task<object> publicGetLastPricePair (object parameters = null)
    {
        return await this.callAsync ("publicGetLastPricePair",parameters);
    }

    public async Task<object> publicGetLastPricesCurrencies (object parameters = null)
    {
        return await this.callAsync ("publicGetLastPricesCurrencies",parameters);
    }

    public async Task<object> publicGetOhlcvHdYyyymmddPair (object parameters = null)
    {
        return await this.callAsync ("publicGetOhlcvHdYyyymmddPair",parameters);
    }

    public async Task<object> publicGetOrderBookPair (object parameters = null)
    {
        return await this.callAsync ("publicGetOrderBookPair",parameters);
    }

    public async Task<object> publicGetTickerPair (object parameters = null)
    {
        return await this.callAsync ("publicGetTickerPair",parameters);
    }

    public async Task<object> publicGetTickersCurrencies (object parameters = null)
    {
        return await this.callAsync ("publicGetTickersCurrencies",parameters);
    }

    public async Task<object> publicGetTradeHistoryPair (object parameters = null)
    {
        return await this.callAsync ("publicGetTradeHistoryPair",parameters);
    }

    public async Task<object> publicPostConvertPair (object parameters = null)
    {
        return await this.callAsync ("publicPostConvertPair",parameters);
    }

    public async Task<object> publicPostPriceStatsPair (object parameters = null)
    {
        return await this.callAsync ("publicPostPriceStatsPair",parameters);
    }

    public async Task<object> privatePostActiveOrdersStatus (object parameters = null)
    {
        return await this.callAsync ("privatePostActiveOrdersStatus",parameters);
    }

    public async Task<object> privatePostArchivedOrdersPair (object parameters = null)
    {
        return await this.callAsync ("privatePostArchivedOrdersPair",parameters);
    }

    public async Task<object> privatePostBalance (object parameters = null)
    {
        return await this.callAsync ("privatePostBalance",parameters);
    }

    public async Task<object> privatePostCancelOrder (object parameters = null)
    {
        return await this.callAsync ("privatePostCancelOrder",parameters);
    }

    public async Task<object> privatePostCancelOrdersPair (object parameters = null)
    {
        return await this.callAsync ("privatePostCancelOrdersPair",parameters);
    }

    public async Task<object> privatePostCancelReplaceOrderPair (object parameters = null)
    {
        return await this.callAsync ("privatePostCancelReplaceOrderPair",parameters);
    }

    public async Task<object> privatePostClosePositionPair (object parameters = null)
    {
        return await this.callAsync ("privatePostClosePositionPair",parameters);
    }

    public async Task<object> privatePostGetAddress (object parameters = null)
    {
        return await this.callAsync ("privatePostGetAddress",parameters);
    }

    public async Task<object> privatePostGetCryptoAddress (object parameters = null)
    {
        return await this.callAsync ("privatePostGetCryptoAddress",parameters);
    }

    public async Task<object> privatePostGetMyfee (object parameters = null)
    {
        return await this.callAsync ("privatePostGetMyfee",parameters);
    }

    public async Task<object> privatePostGetOrder (object parameters = null)
    {
        return await this.callAsync ("privatePostGetOrder",parameters);
    }

    public async Task<object> privatePostGetOrderTx (object parameters = null)
    {
        return await this.callAsync ("privatePostGetOrderTx",parameters);
    }

    public async Task<object> privatePostOpenOrdersPair (object parameters = null)
    {
        return await this.callAsync ("privatePostOpenOrdersPair",parameters);
    }

    public async Task<object> privatePostOpenOrders (object parameters = null)
    {
        return await this.callAsync ("privatePostOpenOrders",parameters);
    }

    public async Task<object> privatePostOpenPositionPair (object parameters = null)
    {
        return await this.callAsync ("privatePostOpenPositionPair",parameters);
    }

    public async Task<object> privatePostOpenPositionsPair (object parameters = null)
    {
        return await this.callAsync ("privatePostOpenPositionsPair",parameters);
    }

    public async Task<object> privatePostPlaceOrderPair (object parameters = null)
    {
        return await this.callAsync ("privatePostPlaceOrderPair",parameters);
    }

    public async Task<object> privatePostRawTxHistory (object parameters = null)
    {
        return await this.callAsync ("privatePostRawTxHistory",parameters);
    }

}