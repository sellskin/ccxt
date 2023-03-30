import idexRest from '../idex.js';
import { Int } from '../base/types.js';
export default class idex extends idexRest {
    describe(): any;
    subscribe(subscribeObject: any, messageHash: any, subscription?: boolean): Promise<any>;
    subscribePrivate(subscribeObject: any, messageHash: any): Promise<any>;
    watchTicker(symbol: string, params?: {}): Promise<any>;
    handleTicker(client: any, message: any): void;
    watchTrades(symbol: string, since?: Int, limit?: Int, params?: {}): Promise<any>;
    handleTrade(client: any, message: any): void;
    parseWsTrade(trade: any): {
        info: any;
        timestamp: number;
        datetime: string;
        symbol: any;
        id: string;
        order: any;
        type: any;
        takerOrMaker: string;
        side: string;
        price: number;
        amount: number;
        cost: number;
        fee: {
            currency: string;
            cost: number;
        };
    };
    watchOHLCV(symbol: string, timeframe?: string, since?: Int, limit?: Int, params?: {}): Promise<any>;
    handleOHLCV(client: any, message: any): void;
    handleSubscribeMessage(client: any, message: any): void;
    fetchOrderBookSnapshot(client: any, symbol: any, params?: {}): Promise<void>;
    watchOrderBook(symbol: string, limit?: Int, params?: {}): Promise<any>;
    handleOrderBook(client: any, message: any): void;
    handleOrderBookMessage(client: any, message: any, orderbook: any): void;
    handleDelta(bookside: any, delta: any): void;
    handleDeltas(bookside: any, deltas: any): void;
    authenticate(params?: {}): Promise<any>;
    watchOrders(symbol?: string, since?: Int, limit?: Int, params?: {}): Promise<any>;
    handleOrder(client: any, message: any): void;
    watchTransactions(code?: any, since?: Int, limit?: Int, params?: {}): Promise<any>;
    handleTransaction(client: any, message: any): void;
    handleMessage(client: any, message: any): void;
}
