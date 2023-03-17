# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.base.exchange import Exchange
from ccxt.base.errors import ExchangeError
from ccxt.base.decimal_to_precision import TICK_SIZE
from ccxt.base.precise import Precise


class paymium(Exchange):

    def describe(self):
        return self.deep_extend(super(paymium, self).describe(), {
            'id': 'paymium',
            'name': 'Paymium',
            'countries': ['FR', 'EU'],
            'rateLimit': 2000,
            'version': 'v1',
            'has': {
                'CORS': True,
                'spot': True,
                'margin': None,
                'swap': False,
                'future': False,
                'option': False,
                'cancelOrder': True,
                'createDepositAddress': True,
                'createOrder': True,
                'fetchBalance': True,
                'fetchDepositAddress': True,
                'fetchDepositAddresses': True,
                'fetchFundingHistory': False,
                'fetchFundingRate': False,
                'fetchFundingRateHistory': False,
                'fetchFundingRates': False,
                'fetchIndexOHLCV': False,
                'fetchMarkOHLCV': False,
                'fetchOpenInterestHistory': False,
                'fetchOrderBook': True,
                'fetchPremiumIndexOHLCV': False,
                'fetchTicker': True,
                'fetchTrades': True,
                'fetchTradingFee': False,
                'fetchTradingFees': False,
                'transfer': True,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/51840849/87153930-f0f02200-c2c0-11ea-9c0a-40337375ae89.jpg',
                'api': {
                    'rest': 'https://paymium.com/api',
                },
                'www': 'https://www.paymium.com',
                'fees': 'https://www.paymium.com/page/help/fees',
                'doc': [
                    'https://github.com/Paymium/api-documentation',
                    'https://www.paymium.com/page/developers',
                    'https://paymium.github.io/api-documentation/',
                ],
                'referral': 'https://www.paymium.com/page/sign-up?referral=eDAzPoRQFMvaAB8sf-qj',
            },
            'api': {
                'public': {
                    'get': [
                        'countries',
                        'data/{currency}/ticker',
                        'data/{currency}/trades',
                        'data/{currency}/depth',
                        'bitcoin_charts/{id}/trades',
                        'bitcoin_charts/{id}/depth',
                    ],
                },
                'private': {
                    'get': [
                        'user',
                        'user/addresses',
                        'user/addresses/{address}',
                        'user/orders',
                        'user/orders/{uuid}',
                        'user/price_alerts',
                        'merchant/get_payment/{uuid}',
                    ],
                    'post': [
                        'user/addresses',
                        'user/orders',
                        'user/withdrawals',
                        'user/email_transfers',
                        'user/payment_requests',
                        'user/price_alerts',
                        'merchant/create_payment',
                    ],
                    'delete': [
                        'user/orders/{uuid}',
                        'user/orders/{uuid}/cancel',
                        'user/price_alerts/{id}',
                    ],
                },
            },
            'markets': {
                'BTC/EUR': {'id': 'eur', 'symbol': 'BTC/EUR', 'base': 'BTC', 'quote': 'EUR', 'baseId': 'btc', 'quoteId': 'eur', 'type': 'spot', 'spot': True},
            },
            'fees': {
                'trading': {
                    'maker': self.parse_number('-0.001'),
                    'taker': self.parse_number('0.005'),
                },
            },
            'precisionMode': TICK_SIZE,
        })

    def parse_balance(self, response):
        result = {'info': response}
        currencies = list(self.currencies.keys())
        for i in range(0, len(currencies)):
            code = currencies[i]
            currency = self.currency(code)
            currencyId = currency['id']
            free = 'balance_' + currencyId
            if free in response:
                account = self.account()
                used = 'locked_' + currencyId
                account['free'] = self.safe_string(response, free)
                account['used'] = self.safe_string(response, used)
                result[code] = account
        return self.safe_balance(result)

    async def fetch_balance(self, params={}):
        """
        query for balance and get the amount of funds available for trading or funds locked in orders
        :param dict params: extra parameters specific to the paymium api endpoint
        :returns dict: a `balance structure <https://docs.ccxt.com/en/latest/manual.html?#balance-structure>`
        """
        await self.load_markets()
        response = await self.privateGetUser(params)
        return self.parse_balance(response)

    async def fetch_order_book(self, symbol, limit=None, params={}):
        """
        fetches information on open orders with bid(buy) and ask(sell) prices, volumes and other data
        :param str symbol: unified symbol of the market to fetch the order book for
        :param int|None limit: the maximum amount of order book entries to return
        :param dict params: extra parameters specific to the paymium api endpoint
        :returns dict: A dictionary of `order book structures <https://docs.ccxt.com/#/?id=order-book-structure>` indexed by market symbols
        """
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'currency': market['id'],
        }
        response = await self.publicGetDataCurrencyDepth(self.extend(request, params))
        return self.parse_order_book(response, market['symbol'], None, 'bids', 'asks', 'price', 'amount')

    def parse_ticker(self, ticker, market=None):
        #
        # {
        #     "high":"33740.82",
        #     "low":"32185.15",
        #     "volume":"4.7890433",
        #     "bid":"33313.53",
        #     "ask":"33497.97",
        #     "midpoint":"33405.75",
        #     "vwap":"32802.5263553",
        #     "at":1643381654,
        #     "price":"33143.91",
        #     "open":"33116.86",
        #     "variation":"0.0817",
        #     "currency":"EUR",
        #     "trade_id":"ce2f5152-3ac5-412d-9b24-9fa72338474c",
        #     "size":"0.00041087"
        # }
        #
        symbol = self.safe_symbol(None, market)
        timestamp = self.safe_timestamp(ticker, 'at')
        vwap = self.safe_string(ticker, 'vwap')
        baseVolume = self.safe_string(ticker, 'volume')
        quoteVolume = Precise.string_mul(baseVolume, vwap)
        last = self.safe_string(ticker, 'price')
        return self.safe_ticker({
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_string(ticker, 'high'),
            'low': self.safe_string(ticker, 'low'),
            'bid': self.safe_string(ticker, 'bid'),
            'bidVolume': None,
            'ask': self.safe_string(ticker, 'ask'),
            'askVolume': None,
            'vwap': vwap,
            'open': self.safe_string(ticker, 'open'),
            'close': last,
            'last': last,
            'previousClose': None,
            'change': None,
            'percentage': self.safe_string(ticker, 'variation'),
            'average': None,
            'baseVolume': baseVolume,
            'quoteVolume': quoteVolume,
            'info': ticker,
        }, market)

    async def fetch_ticker(self, symbol, params={}):
        """
        fetches a price ticker, a statistical calculation with the information calculated over the past 24 hours for a specific market
        :param str symbol: unified symbol of the market to fetch the ticker for
        :param dict params: extra parameters specific to the paymium api endpoint
        :returns dict: a `ticker structure <https://docs.ccxt.com/#/?id=ticker-structure>`
        """
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'currency': market['id'],
        }
        ticker = await self.publicGetDataCurrencyTicker(self.extend(request, params))
        #
        # {
        #     "high":"33740.82",
        #     "low":"32185.15",
        #     "volume":"4.7890433",
        #     "bid":"33313.53",
        #     "ask":"33497.97",
        #     "midpoint":"33405.75",
        #     "vwap":"32802.5263553",
        #     "at":1643381654,
        #     "price":"33143.91",
        #     "open":"33116.86",
        #     "variation":"0.0817",
        #     "currency":"EUR",
        #     "trade_id":"ce2f5152-3ac5-412d-9b24-9fa72338474c",
        #     "size":"0.00041087"
        # }
        #
        return self.parse_ticker(ticker, market)

    def parse_trade(self, trade, market):
        timestamp = self.safe_timestamp(trade, 'created_at_int')
        id = self.safe_string(trade, 'uuid')
        market = self.safe_market(None, market)
        side = self.safe_string(trade, 'side')
        price = self.safe_string(trade, 'price')
        amountField = 'traded_' + market['base'].lower()
        amount = self.safe_string(trade, amountField)
        return self.safe_trade({
            'info': trade,
            'id': id,
            'order': None,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': market['symbol'],
            'type': None,
            'side': side,
            'takerOrMaker': None,
            'price': price,
            'amount': amount,
            'cost': None,
            'fee': None,
        }, market)

    async def fetch_trades(self, symbol, since=None, limit=None, params={}):
        """
        get the list of most recent trades for a particular symbol
        :param str symbol: unified symbol of the market to fetch trades for
        :param int|None since: timestamp in ms of the earliest trade to fetch
        :param int|None limit: the maximum amount of trades to fetch
        :param dict params: extra parameters specific to the paymium api endpoint
        :returns [dict]: a list of `trade structures <https://docs.ccxt.com/en/latest/manual.html?#public-trades>`
        """
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'currency': market['id'],
        }
        response = await self.publicGetDataCurrencyTrades(self.extend(request, params))
        return self.parse_trades(response, market, since, limit)

    async def create_deposit_address(self, code, params={}):
        """
        create a currency deposit address
        :param str code: unified currency code of the currency for the deposit address
        :param dict params: extra parameters specific to the paymium api endpoint
        :returns dict: an `address structure <https://docs.ccxt.com/#/?id=address-structure>`
        """
        await self.load_markets()
        response = await self.privatePostUserAddresses(params)
        #
        #     {
        #         "address": "1HdjGr6WCTcnmW1tNNsHX7fh4Jr5C2PeKe",
        #         "valid_until": 1620041926,
        #         "currency": "BTC",
        #         "label": "Savings"
        #     }
        #
        return self.parse_deposit_address(response)

    async def fetch_deposit_address(self, code, params={}):
        """
        fetch the deposit address for a currency associated with self account
        :param str code: unified currency code
        :param dict params: extra parameters specific to the paymium api endpoint
        :returns dict: an `address structure <https://docs.ccxt.com/#/?id=address-structure>`
        """
        await self.load_markets()
        request = {
            'address': code,
        }
        response = await self.privateGetUserAddressesAddress(self.extend(request, params))
        #
        #     {
        #         "address": "1HdjGr6WCTcnmW1tNNsHX7fh4Jr5C2PeKe",
        #         "valid_until": 1620041926,
        #         "currency": "BTC",
        #         "label": "Savings"
        #     }
        #
        return self.parse_deposit_address(response)

    async def fetch_deposit_addresses(self, codes=None, params={}):
        """
        fetch deposit addresses for multiple currencies and chain types
        :param [str]|None codes: list of unified currency codes, default is None
        :param dict params: extra parameters specific to the paymium api endpoint
        :returns dict: a list of `address structures <https://docs.ccxt.com/#/?id=address-structure>`
        """
        await self.load_markets()
        response = await self.privateGetUserAddresses(params)
        #
        #     [
        #         {
        #             "address": "1HdjGr6WCTcnmW1tNNsHX7fh4Jr5C2PeKe",
        #             "valid_until": 1620041926,
        #             "currency": "BTC",
        #             "label": "Savings"
        #         }
        #     ]
        #
        return self.parse_deposit_addresses(response, codes)

    def parse_deposit_address(self, depositAddress, currency=None):
        #
        #     {
        #         "address": "1HdjGr6WCTcnmW1tNNsHX7fh4Jr5C2PeKe",
        #         "valid_until": 1620041926,
        #         "currency": "BTC",
        #         "label": "Savings"
        #     }
        #
        address = self.safe_string(depositAddress, 'address')
        currencyId = self.safe_string(depositAddress, 'currency')
        return {
            'info': depositAddress,
            'currency': self.safe_currency_code(currencyId, currency),
            'address': address,
            'tag': None,
            'network': None,
        }

    async def create_order(self, symbol, type, side, amount, price=None, params={}):
        """
        create a trade order
        :param str symbol: unified symbol of the market to create an order in
        :param str type: 'market' or 'limit'
        :param str side: 'buy' or 'sell'
        :param float amount: how much of currency you want to trade in units of base currency
        :param float|None price: the price at which the order is to be fullfilled, in units of the quote currency, ignored in market orders
        :param dict params: extra parameters specific to the paymium api endpoint
        :returns dict: an `order structure <https://docs.ccxt.com/#/?id=order-structure>`
        """
        await self.load_markets()
        market = self.market(symbol)
        request = {
            'type': self.capitalize(type) + 'Order',
            'currency': market['id'],
            'direction': side,
            'amount': amount,
        }
        if type != 'market':
            request['price'] = price
        response = await self.privatePostUserOrders(self.extend(request, params))
        return self.safe_order({
            'info': response,
            'id': response['uuid'],
        }, market)

    async def cancel_order(self, id, symbol=None, params={}):
        """
        cancels an open order
        :param str id: order id
        :param str|None symbol: not used by paymium cancelOrder()
        :param dict params: extra parameters specific to the paymium api endpoint
        :returns dict: An `order structure <https://docs.ccxt.com/#/?id=order-structure>`
        """
        request = {
            'uuid': id,
        }
        return await self.privateDeleteUserOrdersUuidCancel(self.extend(request, params))

    async def transfer(self, code, amount, fromAccount, toAccount, params={}):
        """
        transfer currency internally between wallets on the same account
        :param str code: unified currency code
        :param float amount: amount to transfer
        :param str fromAccount: account to transfer from
        :param str toAccount: account to transfer to
        :param dict params: extra parameters specific to the paymium api endpoint
        :returns dict: a `transfer structure <https://docs.ccxt.com/#/?id=transfer-structure>`
        """
        await self.load_markets()
        currency = self.currency(code)
        if toAccount.find('@') < 0:
            raise ExchangeError(self.id + ' transfer() only allows transfers to an email address')
        if code != 'BTC' and code != 'EUR':
            raise ExchangeError(self.id + ' transfer() only allows BTC or EUR')
        request = {
            'currency': currency['id'],
            'amount': self.currency_to_precision(code, amount),
            'email': toAccount,
            # 'comment': 'a small note explaining the transfer'
        }
        response = await self.privatePostUserEmailTransfers(self.extend(request, params))
        #
        #     {
        #         "uuid": "968f4580-e26c-4ad8-8bcd-874d23d55296",
        #         "type": "Transfer",
        #         "currency": "BTC",
        #         "currency_amount": "string",
        #         "created_at": "2013-10-24T10:34:37.000Z",
        #         "updated_at": "2013-10-24T10:34:37.000Z",
        #         "amount": "1.0",
        #         "state": "executed",
        #         "currency_fee": "0.0",
        #         "btc_fee": "0.0",
        #         "comment": "string",
        #         "traded_btc": "string",
        #         "traded_currency": "string",
        #         "direction": "buy",
        #         "price": "string",
        #         "account_operations": [
        #             {
        #                 "uuid": "968f4580-e26c-4ad8-8bcd-874d23d55296",
        #                 "amount": "1.0",
        #                 "currency": "BTC",
        #                 "created_at": "2013-10-24T10:34:37.000Z",
        #                 "created_at_int": 1389094259,
        #                 "name": "account_operation",
        #                 "address": "1FPDBXNqSkZMsw1kSkkajcj8berxDQkUoc",
        #                 "tx_hash": "string",
        #                 "is_trading_account": True
        #             }
        #         ]
        #     }
        #
        return self.parse_transfer(response, currency)

    def parse_transfer(self, transfer, currency=None):
        #
        #     {
        #         "uuid": "968f4580-e26c-4ad8-8bcd-874d23d55296",
        #         "type": "Transfer",
        #         "currency": "BTC",
        #         "currency_amount": "string",
        #         "created_at": "2013-10-24T10:34:37.000Z",
        #         "updated_at": "2013-10-24T10:34:37.000Z",
        #         "amount": "1.0",
        #         "state": "executed",
        #         "currency_fee": "0.0",
        #         "btc_fee": "0.0",
        #         "comment": "string",
        #         "traded_btc": "string",
        #         "traded_currency": "string",
        #         "direction": "buy",
        #         "price": "string",
        #         "account_operations": [
        #             {
        #                 "uuid": "968f4580-e26c-4ad8-8bcd-874d23d55296",
        #                 "amount": "1.0",
        #                 "currency": "BTC",
        #                 "created_at": "2013-10-24T10:34:37.000Z",
        #                 "created_at_int": 1389094259,
        #                 "name": "account_operation",
        #                 "address": "1FPDBXNqSkZMsw1kSkkajcj8berxDQkUoc",
        #                 "tx_hash": "string",
        #                 "is_trading_account": True
        #             }
        #         ]
        #     }
        #
        currencyId = self.safe_string(transfer, 'currency')
        updatedAt = self.safe_string(transfer, 'updated_at')
        timetstamp = self.parse_date(updatedAt)
        accountOperations = self.safe_value(transfer, 'account_operations')
        firstOperation = self.safe_value(accountOperations, 0, {})
        status = self.safe_string(transfer, 'state')
        return {
            'info': transfer,
            'id': self.safe_string(transfer, 'uuid'),
            'timestamp': timetstamp,
            'datetime': self.iso8601(timetstamp),
            'currency': self.safe_currency_code(currencyId, currency),
            'amount': self.safe_number(transfer, 'amount'),
            'fromAccount': None,
            'toAccount': self.safe_string(firstOperation, 'address'),
            'status': self.parse_transfer_status(status),
        }

    def parse_transfer_status(self, status):
        statuses = {
            'executed': 'ok',
            # what are the other statuses?
        }
        return self.safe_string(statuses, status, status)

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api']['rest'] + '/' + self.version + '/' + self.implode_params(path, params)
        query = self.omit(params, self.extract_params(path))
        if api == 'public':
            if query:
                url += '?' + self.urlencode(query)
        else:
            self.check_required_credentials()
            nonce = str(self.nonce())
            auth = nonce + url
            headers = {
                'Api-Key': self.apiKey,
                'Api-Nonce': nonce,
            }
            if method == 'POST':
                if query:
                    body = self.json(query)
                    auth += body
                    headers['Content-Type'] = 'application/json'
            else:
                if query:
                    queryString = self.urlencode(query)
                    auth += queryString
                    url += '?' + queryString
            headers['Api-Signature'] = self.hmac(self.encode(auth), self.encode(self.secret))
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, httpCode, reason, url, method, headers, body, response, requestHeaders, requestBody):
        if response is None:
            return
        errors = self.safe_value(response, 'errors')
        if errors is not None:
            raise ExchangeError(self.id + ' ' + self.json(response))
