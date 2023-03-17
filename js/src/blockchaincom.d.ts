import { Exchange } from './base/Exchange.js';
export default class blockchaincom extends Exchange {
    describe(): any;
    fetchMarkets(params?: {}): Promise<any[]>;
    fetchOrderBook(symbol: any, limit?: any, params?: {}): Promise<import("./base/types.js").OrderBook>;
    fetchL3OrderBook(symbol: any, limit?: any, params?: {}): Promise<import("./base/types.js").OrderBook>;
    fetchL2OrderBook(symbol: any, limit?: any, params?: {}): Promise<import("./base/types.js").OrderBook>;
    parseTicker(ticker: any, market?: any): import("./base/types.js").Ticker;
    fetchTicker(symbol: any, params?: {}): Promise<import("./base/types.js").Ticker>;
    fetchTickers(symbols?: string[], params?: {}): Promise<any>;
    parseOrderState(state: any): string;
    parseOrder(order: any, market?: any): any;
    createOrder(symbol: any, type: any, side: any, amount: any, price?: any, params?: {}): Promise<any>;
    cancelOrder(id: any, symbol?: string, params?: {}): Promise<{
        id: any;
        info: any;
    }>;
    cancelAllOrders(symbol?: string, params?: {}): Promise<{
        symbol: string;
        info: any;
    }>;
    fetchTradingFees(params?: {}): Promise<{}>;
    fetchCanceledOrders(symbol?: string, since?: any, limit?: any, params?: {}): Promise<import("./base/types.js").Order[]>;
    fetchClosedOrders(symbol?: string, since?: any, limit?: any, params?: {}): Promise<import("./base/types.js").Order[]>;
    fetchOpenOrders(symbol?: string, since?: any, limit?: any, params?: {}): Promise<import("./base/types.js").Order[]>;
    fetchOrdersByState(state: any, symbol?: string, since?: any, limit?: any, params?: {}): Promise<import("./base/types.js").Order[]>;
    parseTrade(trade: any, market?: any): import("./base/types.js").Trade;
    fetchMyTrades(symbol?: string, since?: any, limit?: any, params?: {}): Promise<import("./base/types.js").Trade[]>;
    fetchDepositAddress(code: any, params?: {}): Promise<{
        info: any;
    }>;
    parseTransactionState(state: any): string;
    parseTransaction(transaction: any, currency?: any): {
        info: any;
        id: any;
        txid: string;
        timestamp: number;
        datetime: string;
        network: any;
        addressFrom: any;
        address: string;
        addressTo: string;
        tagFrom: any;
        tag: any;
        tagTo: any;
        type: any;
        amount: number;
        currency: any;
        status: string;
        updated: any;
        comment: any;
        fee: any;
    };
    fetchWithdrawalWhitelist(params?: {}): Promise<any[]>;
    fetchWithdrawalWhitelistByCurrency(code: any, params?: {}): Promise<any[]>;
    withdraw(code: any, amount: any, address: any, tag?: any, params?: {}): Promise<{
        info: any;
        id: any;
        txid: string;
        timestamp: number;
        datetime: string;
        network: any;
        addressFrom: any;
        address: string;
        addressTo: string;
        tagFrom: any;
        tag: any;
        tagTo: any;
        type: any;
        amount: number;
        currency: any;
        status: string;
        updated: any;
        comment: any;
        fee: any;
    }>;
    fetchWithdrawals(code?: string, since?: any, limit?: any, params?: {}): Promise<any>;
    fetchWithdrawal(id: any, code?: any, params?: {}): Promise<{
        info: any;
        id: any;
        txid: string;
        timestamp: number;
        datetime: string;
        network: any;
        addressFrom: any;
        address: string;
        addressTo: string;
        tagFrom: any;
        tag: any;
        tagTo: any;
        type: any;
        amount: number;
        currency: any;
        status: string;
        updated: any;
        comment: any;
        fee: any;
    }>;
    fetchDeposits(code?: string, since?: any, limit?: any, params?: {}): Promise<any>;
    fetchDeposit(id: any, code?: any, params?: {}): Promise<{
        info: any;
        id: any;
        txid: string;
        timestamp: number;
        datetime: string;
        network: any;
        addressFrom: any;
        address: string;
        addressTo: string;
        tagFrom: any;
        tag: any;
        tagTo: any;
        type: any;
        amount: number;
        currency: any;
        status: string;
        updated: any;
        comment: any;
        fee: any;
    }>;
    fetchBalance(params?: {}): Promise<import("./base/types.js").Balances>;
    fetchOrder(id: any, symbol?: string, params?: {}): Promise<any>;
    sign(path: any, api?: any, method?: string, params?: {}, headers?: any, body?: any): {
        url: string;
        method: string;
        body: any;
        headers: any;
    };
    handleErrors(code: any, reason: any, url: any, method: any, headers: any, body: any, response: any, requestHeaders: any, requestBody: any): void;
}
