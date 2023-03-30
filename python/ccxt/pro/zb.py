# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

import ccxt.async_support
from ccxt.async_support.base.ws.cache import ArrayCache, ArrayCacheByTimestamp
from typing import Optional
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import NotSupported
from ccxt.base.errors import AuthenticationError


class zb(ccxt.async_support.zb):

    def describe(self):
        return self.deep_extend(super(zb, self).describe(), {
            'has': {
                'ws': True,
                'watchOrderBook': True,
                'watchTicker': True,
                'watchTrades': True,
                'watchOHLCV': True,
            },
            'urls': {
                'api': {
                    'ws': {
                        'spot': 'wss://api.{hostname}/websocket',
                        'contract': 'wss://fapi.{hostname}/ws/public/v1',
                    },
                },
            },
            'options': {
                'tradesLimit': 1000,
                'ordersLimit': 1000,
                'OHLCVLimit': 1000,
            },
        })

    async def watch_public(self, url, messageHash, symbol, method, limit: Optional[int] = None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        type = 'spot' if market['spot'] else 'contract'
        request = None
        isLimitSet = limit is not None
        if type == 'spot':
            request = {
                'event': 'addChannel',
                'channel': messageHash,
            }
            if isLimitSet:
                request['length'] = limit
        else:
            request = {
                'action': 'subscribe',
                'channel': messageHash,
            }
            if isLimitSet:
                request['size'] = limit
        message = self.extend(request, params)
        subscription = {
            'symbol': symbol,
            'messageHash': messageHash,
            'method': method,
        }
        if isLimitSet:
            subscription['limit'] = limit
        return await self.watch(url, messageHash, message, messageHash, subscription)

    async def watch_ticker(self, symbol: str, params={}):
        await self.load_markets()
        market = self.market(symbol)
        messageHash = None
        type = 'spot' if market['spot'] else 'contract'
        if type == 'spot':
            messageHash = market['baseId'] + market['quoteId'] + '_' + 'ticker'
        else:
            messageHash = market['id'] + '.' + 'Ticker'
        url = self.implode_hostname(self.urls['api']['ws'][type])
        return await self.watch_public(url, messageHash, symbol, self.handle_ticker, None, params)

    def parse_ws_ticker(self, ticker, market=None):
        #
        # contract ticker
        #      {
        #          data: [
        #            38568.36,  # open
        #            39958.75,  # high
        #            38100,  # low
        #            39211.78,  # last
        #            61695.496,  # volume 24h
        #            1.67,  # change
        #            1647369457,  # time
        #            285916.615048
        #          ]
        #    }
        #
        timestamp = self.safe_integer(ticker, 6)
        last = self.safe_string(ticker, 3)
        return self.safe_ticker({
            'symbol': self.safe_symbol(None, market),
            'timestamp': timestamp,
            'datetime': None,
            'high': self.safe_string(ticker, 1),
            'low': self.safe_string(ticker, 2),
            'bid': None,
            'bidVolume': None,
            'ask': None,
            'askVolume': None,
            'vwap': None,
            'open': self.safe_string(ticker, 0),
            'close': last,
            'last': last,
            'previousClose': None,
            'change': None,
            'percentage': self.safe_string(ticker, 5),
            'average': None,
            'baseVolume': self.safe_string(ticker, 4),
            'quoteVolume': None,
            'info': ticker,
        }, market)

    def handle_ticker(self, client, message, subscription):
        #
        # spot ticker
        #
        #     {
        #         date: '1624398991255',
        #         ticker: {
        #             high: '33298.38',
        #             vol: '56375.9469',
        #             last: '32396.95',
        #             low: '28808.19',
        #             buy: '32395.81',
        #             sell: '32409.3',
        #             turnover: '1771122527.0000',
        #             open: '31652.44',
        #             riseRate: '2.36'
        #         },
        #         dataType: 'ticker',
        #         channel: 'btcusdt_ticker'
        #     }
        #
        # contract ticker
        #      {
        #          channel: 'BTC_USDT.Ticker',
        #          data: [
        #            38568.36,
        #            39958.75,
        #            38100,
        #            39211.78,
        #            61695.496,
        #            1.67,
        #            1647369457,
        #            285916.615048
        #          ]
        #      }
        #
        symbol = self.safe_string(subscription, 'symbol')
        channel = self.safe_string(message, 'channel')
        market = self.market(symbol)
        data = self.safe_value(message, 'ticker')
        ticker = None
        if data is None:
            data = self.safe_value(message, 'data', [])
            ticker = self.parse_ws_ticker(data, market)
        else:
            data['date'] = self.safe_value(message, 'date')
            ticker = self.parse_ticker(data, market)
        ticker['symbol'] = symbol
        self.tickers[symbol] = ticker
        client.resolve(ticker, channel)
        return message

    async def watch_ohlcv(self, symbol: str, timeframe='1m', since: Optional[int] = None, limit: Optional[int] = None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        if market['spot']:
            raise NotSupported(self.id + ' watchOHLCV() supports contract markets only')
        if (limit is None) or (limit > 1440):
            limit = 100
        interval = self.safe_string(self.timeframes, timeframe, timeframe)
        messageHash = market['id'] + '.KLine' + '_' + interval
        url = self.implode_hostname(self.urls['api']['ws']['contract'])
        ohlcv = await self.watch_public(url, messageHash, symbol, self.handle_ohlcv, limit, params)
        if self.newUpdates:
            limit = ohlcv.getLimit(symbol, limit)
        return self.filter_by_since_limit(ohlcv, since, limit, 0, True)

    def handle_ohlcv(self, client, message, subscription):
        #
        # snapshot update
        #    {
        #        channel: 'BTC_USDT.KLine_1m',
        #        type: 'Whole',
        #        data: [
        #          [48543.77, 48543.77, 48542.82, 48542.82, 0.43, 1640227260],
        #          [48542.81, 48542.81, 48529.89, 48529.89, 1.202, 1640227320],
        #          [48529.95, 48529.99, 48529.85, 48529.9, 4.226, 1640227380],
        #          [48529.96, 48529.99, 48525.11, 48525.11, 8.858, 1640227440],
        #          [48525.05, 48525.05, 48464.17, 48476.63, 32.772, 1640227500],
        #          [48475.62, 48485.65, 48475.12, 48479.36, 20.04, 1640227560],
        #        ]
        #    }
        # partial update
        #    {
        #        channel: 'BTC_USDT.KLine_1m',
        #        data: [
        #          [39095.45, 45339.48, 36923.58, 39204.94, 1215304.988, 1645920000]
        #        ]
        #    }
        #
        data = self.safe_value(message, 'data', [])
        channel = self.safe_string(message, 'channel', '')
        parts = channel.split('_')
        partsLength = len(parts)
        interval = self.safe_string(parts, partsLength - 1)
        timeframe = self.find_timeframe(interval)
        symbol = self.safe_string(subscription, 'symbol')
        market = self.market(symbol)
        for i in range(0, len(data)):
            candle = data[i]
            parsed = self.parse_ohlcv(candle, market)
            self.ohlcvs[symbol] = self.safe_value(self.ohlcvs, symbol, {})
            stored = self.safe_value(self.ohlcvs[symbol], timeframe)
            if stored is None:
                limit = self.safe_integer(self.options, 'OHLCVLimit', 1000)
                stored = ArrayCacheByTimestamp(limit)
                self.ohlcvs[symbol][timeframe] = stored
            stored.append(parsed)
            client.resolve(stored, channel)
        return message

    async def watch_trades(self, symbol: str, since: Optional[int] = None, limit: Optional[int] = None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        messageHash = None
        type = 'spot' if market['spot'] else 'contract'
        if type == 'spot':
            messageHash = market['baseId'] + market['quoteId'] + '_' + 'trades'
        else:
            messageHash = market['id'] + '.' + 'Trade'
        url = self.implode_hostname(self.urls['api']['ws'][type])
        trades = await self.watch_public(url, messageHash, symbol, self.handle_trades, limit, params)
        if self.newUpdates:
            limit = trades.getLimit(symbol, limit)
        return self.filter_by_since_limit(trades, since, limit, 'timestamp', True)

    def handle_trades(self, client, message, subscription):
        # contract trades
        # {
        #     "channel":"BTC_USDT.Trade",
        #     "type":"Whole",
        #     "data":[
        #        [
        #           40768.07,
        #           0.01,
        #           1,
        #           1647442757
        #        ],
        #        [
        #           40792.22,
        #           0.334,
        #           -1,
        #           1647442765
        #        ],
        #        [
        #           40789.77,
        #           0.14,
        #           1,
        #           1647442766
        #        ]
        #     ]
        #  }
        # spot trades
        #
        #     {
        #         data: [
        #             {date: 1624537147, amount: '0.0357', price: '34066.11', trade_type: 'bid', type: 'buy', tid: 1718857158},
        #             {date: 1624537147, amount: '0.0255', price: '34071.04', trade_type: 'bid', type: 'buy', tid: 1718857159},
        #             {date: 1624537147, amount: '0.0153', price: '34071.29', trade_type: 'bid', type: 'buy', tid: 1718857160}
        #         ],
        #         dataType: 'trades',
        #         channel: 'btcusdt_trades'
        #     }
        #
        channel = self.safe_value(message, 'channel')
        symbol = self.safe_string(subscription, 'symbol')
        market = self.market(symbol)
        data = self.safe_value(message, 'data')
        type = self.safe_string(message, 'type')
        trades = []
        if type == 'Whole':
            # contract trades
            for i in range(0, len(data)):
                trade = data[i]
                parsed = self.parse_ws_trade(trade, market)
                trades.append(parsed)
        else:
            # spot trades
            trades = self.parse_trades(data, market)
        array = self.safe_value(self.trades, symbol)
        if array is None:
            limit = self.safe_integer(self.options, 'tradesLimit', 1000)
            array = ArrayCache(limit)
        for i in range(0, len(trades)):
            array.append(trades[i])
        self.trades[symbol] = array
        client.resolve(array, channel)

    async def watch_order_book(self, symbol: str, limit: Optional[int] = None, params={}):
        if limit is not None:
            if (limit != 5) and (limit != 10):
                raise ExchangeError(self.id + ' watchOrderBook limit argument must be None, 5, or 10')
        else:
            limit = 5  # default
        await self.load_markets()
        market = self.market(symbol)
        type = 'spot' if market['spot'] else 'contract'
        messageHash = None
        url = self.implode_hostname(self.urls['api']['ws'][type])
        if type == 'spot':
            url += '/' + market['baseId']
            messageHash = market['baseId'] + market['quoteId'] + '_' + 'quick_depth'
        else:
            messageHash = market['id'] + '.' + 'Depth'
        orderbook = await self.watch_public(url, messageHash, symbol, self.handle_order_book, limit, params)
        return orderbook.limit()

    def parse_ws_trade(self, trade, market=None):
        #
        #    [
        #       40768.07,  # price
        #       0.01,  # quantity
        #       1,  # buy or -1 sell
        #       1647442757  # time
        #    ],
        #
        timestamp = self.safe_timestamp(trade, 3)
        price = self.safe_string(trade, 0)
        amount = self.safe_string(trade, 1)
        market = self.safe_market(None, market)
        sideNumber = self.safe_integer(trade, 2)
        side = 'buy' if (sideNumber == 1) else 'sell'
        return self.safe_trade({
            'id': None,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': market['symbol'],
            'order': None,
            'type': None,
            'side': side,
            'takerOrMaker': None,
            'price': price,
            'amount': amount,
            'cost': None,
            'fee': None,
            'info': trade,
        }, market)

    def handle_order_book(self, client, message, subscription):
        # spot snapshot
        #
        #     {
        #         lastTime: 1624524640066,
        #         dataType: 'quickDepth',
        #         channel: 'btcusdt_quick_depth',
        #         currentPrice: 33183.79,
        #         listDown: [
        #             [33166.87, 0.2331],
        #             [33166.86, 0.15],
        #             [33166.76, 0.15],
        #             [33161.02, 0.212],
        #             [33146.35, 0.6066]
        #         ],
        #         market: 'btcusdt',
        #         listUp: [
        #             [33186.88, 0.15],
        #             [33190.1, 0.15],
        #             [33193.03, 0.2518],
        #             [33195.05, 0.2031],
        #             [33199.99, 0.6066]
        #         ],
        #         high: 34816.8,
        #         rate: '6.484',
        #         low: 32312.41,
        #         currentIsBuy: True,
        #         dayNumber: 26988.5536,
        #         totalBtc: 26988.5536,
        #         showMarket: 'btcusdt'
        #     }
        #
        # contract snapshot
        # {
        #     channel: 'BTC_USDT.Depth',
        #     type: 'Whole',
        #     data: {
        #       asks: [[Array], [Array], [Array], [Array], [Array]],
        #       bids: [[Array], [Array], [Array], [Array], [Array]],
        #       time: '1647359998198'
        #     }
        #   }
        #
        # contract deltas
        # {
        #     channel: 'BTC_USDT.Depth',
        #     data: {
        #       bids: [[Array], [Array], [Array], [Array]],
        #       asks: [[Array], [Array], [Array]],
        #       time: '1647360038079'
        #     }
        #  }
        #
        # For contract markets zb will:
        # 1: send snapshot
        # 2: send deltas
        # 3: repeat 1-2
        # So we have a guarentee that deltas
        # are always updated and arrive after
        # the snapshot
        #
        type = self.safe_string_2(message, 'type', 'dataType')
        channel = self.safe_string(message, 'channel')
        symbol = self.safe_string(subscription, 'symbol')
        orderbook = self.safe_value(self.orderbooks, symbol)
        if type is not None:
            # handle orderbook snapshot
            isContractSnapshot = (type == 'Whole')
            data = self.safe_value(message, 'data') if isContractSnapshot else message
            timestamp = self.safe_integer_2(data, 'lastTime', 'time')
            asksKey = 'asks' if isContractSnapshot else 'listUp'
            bidsKey = 'bids' if isContractSnapshot else 'listDown'
            snapshot = self.parse_order_book(data, symbol, timestamp, bidsKey, asksKey)
            if not (symbol in self.orderbooks):
                defaultLimit = self.safe_integer(self.options, 'watchOrderBookLimit', 1000)
                limit = self.safe_integer(subscription, 'limit', defaultLimit)
                orderbook = self.order_book(snapshot, limit)
                self.orderbooks[symbol] = orderbook
            else:
                orderbook = self.orderbooks[symbol]
                orderbook.reset(snapshot)
            orderbook['symbol'] = symbol
            client.resolve(orderbook, channel)
        else:
            self.handle_order_book_message(client, message, orderbook)
            client.resolve(orderbook, channel)

    def handle_order_book_message(self, client, message, orderbook):
        #
        # {
        #     channel: 'BTC_USDT.Depth',
        #     data: {
        #       bids: [[Array], [Array], [Array], [Array]],
        #       asks: [[Array], [Array], [Array]],
        #       time: '1647360038079'
        #     }
        #  }
        #
        data = self.safe_value(message, 'data', {})
        timestamp = self.safe_integer(data, 'time')
        asks = self.safe_value(data, 'asks', [])
        bids = self.safe_value(data, 'bids', [])
        self.handle_deltas(orderbook['asks'], asks)
        self.handle_deltas(orderbook['bids'], bids)
        orderbook['timestamp'] = timestamp
        orderbook['datetime'] = self.iso8601(timestamp)
        return orderbook

    def handle_delta(self, bookside, delta):
        price = self.safe_float(delta, 0)
        amount = self.safe_float(delta, 1)
        bookside.store(price, amount)

    def handle_deltas(self, bookside, deltas):
        for i in range(0, len(deltas)):
            self.handle_delta(bookside, deltas[i])

    def handle_message(self, client, message):
        #
        #
        #     {
        #         no: '0',
        #         code: 1007,
        #         success: False,
        #         channel: 'btc_usdt_ticker',
        #         message: 'Channel is empty'
        #     }
        #
        #     {
        #         date: '1624398991255',
        #         ticker: {
        #             high: '33298.38',
        #             vol: '56375.9469',
        #             last: '32396.95',
        #             low: '28808.19',
        #             buy: '32395.81',
        #             sell: '32409.3',
        #             turnover: '1771122527.0000',
        #             open: '31652.44',
        #             riseRate: '2.36'
        #         },
        #         dataType: 'ticker',
        #         channel: 'btcusdt_ticker'
        #     }
        #
        #     {
        #         data: [
        #             {date: 1624537147, amount: '0.0357', price: '34066.11', trade_type: 'bid', type: 'buy', tid: 1718857158},
        #             {date: 1624537147, amount: '0.0255', price: '34071.04', trade_type: 'bid', type: 'buy', tid: 1718857159},
        #             {date: 1624537147, amount: '0.0153', price: '34071.29', trade_type: 'bid', type: 'buy', tid: 1718857160}
        #         ],
        #         dataType: 'trades',
        #         channel: 'btcusdt_trades'
        #     }
        #
        # contract snapshot
        #
        # {
        #     channel: 'BTC_USDT.Depth',
        #     type: 'Whole',
        #     data: {
        #       asks: [[Array], [Array], [Array], [Array], [Array]],
        #       bids: [[Array], [Array], [Array], [Array], [Array]],
        #       time: '1647359998198'
        #     }
        #   }
        #
        # contract deltas update
        # {
        #     channel: 'BTC_USDT.Depth',
        #     data: {
        #       bids: [[Array], [Array], [Array], [Array]],
        #       asks: [[Array], [Array], [Array]],
        #       time: '1647360038079'
        #     }
        #   }
        #
        channel = self.safe_string(message, 'channel')
        subscription = self.safe_value(client.subscriptions, channel)
        if subscription is not None:
            method = self.safe_value(subscription, 'method')
            if method is not None:
                return method(client, message, subscription)
        return message

    def handle_error_message(self, client, message):
        #
        # {errorCode: 10020, errorMsg: "action param can't be empty"}
        # {errorCode: 10015, errorMsg: '无效的签名(1002)'}
        #
        errorCode = self.safe_string(message, 'errorCode')
        try:
            if errorCode is not None:
                feedback = self.id + ' ' + self.json(message)
                self.throw_exactly_matched_exception(self.exceptions['exact'], errorCode, feedback)
                messageString = self.safe_value(message, 'message')
                if messageString is not None:
                    self.throw_broadly_matched_exception(self.exceptions['broad'], messageString, feedback)
        except Exception as e:
            if isinstance(e, AuthenticationError):
                client.reject(e, 'authenticated')
                method = 'login'
                if method in client.subscriptions:
                    del client.subscriptions[method]
                return False
        return message
