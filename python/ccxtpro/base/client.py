# import json
from asyncio import sleep, ensure_future, wait_for, gather, TimeoutError
from ccxt.async_support import Exchange
from ccxt import NetworkError, RequestTimeout, NotSupported
from ccxtpro.base.future import Future


class Client(object):

    url = None
    ws = None
    futures = {}
    subscriptions = {}
    on_message_callback = None
    on_error_callback = None
    on_close_callback = None
    keepAlive = 3000
    connectionTimeout = 10000  # 10 seconds by default, false to disable
    connection = None
    error = None  # low-level networking exception, if any

    def __init__(self, url, on_message_callback, on_error_callback, on_close_callback, config={}):
        defaults = {
            'url': url,
            'futures': {},
            'subscriptions': {},
            'on_message_callback': on_message_callback,
            'on_error_callback': on_error_callback,
            'on_close_callback': on_close_callback,
            'protocols': None,  # ws-specific protocols
            'options': None,  # ws-specific options
            'connectionStarted': None,  # initiation timestamp in milliseconds
            'connectionEstablished': None,  # success timestamp in milliseconds
            'connectionTimeout': 5000,  # 10 seconds by default, false to disable
            'keepAlive': 3000,  # ping-pong keep-alive frequency
            # timeout is not used atm
            # timeout: 30000,  # throw if a request is not satisfied in 30 seconds, false to disable
        }
        settings = {}
        settings.update(defaults)
        settings.update(config)
        for key in settings:
            if hasattr(self, key) and isinstance(getattr(self, key), dict):
                setattr(self, key, Exchange.deep_extend(getattr(self, key), settings[key]))
            else:
                setattr(self, key, settings[key])
        # connection-related Future
        self.connected = Future()

    def future(self, message_hash):
        if message_hash not in self.futures:
            self.futures[message_hash] = Future()
        return self.futures[message_hash]

    def resolve(self, result, message_hash=None):
        if message_hash:
            if message_hash in self.futures:
                future = self.futures[message_hash]
                future.resolve(result)
                del self.futures[message_hash]
        else:
            message_hashes = list(self.futures.keys())
            for message_hash in message_hashes:
                self.resolve(result, message_hash)
        return result

    def reject(self, result, message_hash=None):
        if message_hash:
            if message_hash in self.futures:
                future = self.futures[message_hash]
                future.reject(result)
                del self.futures[message_hash]
        else:
            message_hashes = list(self.futures.keys())
            for message_hash in message_hashes:
                self.reject(result, message_hash)
        return result

    async def receive_loop(self):
        print(Exchange.iso8601(Exchange.milliseconds()), 'receive loop')
        while not self.closed():
            try:
                message = await self.receive()
                await self.handle_message(message)
            except Exception as e:
                error = NetworkError(e)
                print(Exchange.iso8601(Exchange.milliseconds()), 'receive_loop', 'Exception', error)
                self.reset(error)

    async def open(self, session, backoff_delay=0):
        # exponential backoff for consequent connections if necessary
        if backoff_delay:
            await sleep(backoff_delay)
        print(Exchange.iso8601(Exchange.milliseconds()), 'connecting with timeout', self.connectionTimeout, 'ms')
        self.connectionStarted = Exchange.milliseconds()
        try:
            coroutine = self.create_connection(session)
            self.connection = await wait_for(coroutine, timeout=int(self.connectionTimeout / 1000))
            print(Exchange.iso8601(Exchange.milliseconds()), 'connected')
            self.connected.resolve()
            # run both loops forever
            await gather(self.ping_loop(), self.receive_loop())
        except TimeoutError as e:
            # connection timeout
            error = RequestTimeout('Connection timeout')
            print(Exchange.iso8601(Exchange.milliseconds()), 'RequestTimeout', error)
            self.on_error(error)
        except Exception as e:
            # connection failed or rejected (ConnectionRefusedError, ClientConnectorError)
            error = NetworkError(e)
            print(Exchange.iso8601(Exchange.milliseconds()), 'NetworkError', error)
            self.on_error(error)

    def connect(self, session, backoff_delay=0):
        if not self.connection:
            self.connection = True
            ensure_future(self.open(session, backoff_delay))
        return self.connected

    def on_error(self, error):
        print(Exchange.iso8601(Exchange.milliseconds()), 'on_error', error)
        self.error = error
        self.reset(error)
        self.on_error_callback(self, error)
        if not self.closed():
            ensure_future(self.close(1006))

    def on_close(self, code):
        print(Exchange.iso8601(Exchange.milliseconds()), 'on_close', code)
        if not self.error:
            self.reset(NetworkError(code))
        self.on_close_callback(self, code)
        if not self.closed():
            ensure_future(self.close(code))

    def reset(self, error):
        self.connected.reject(error)
        self.reject(error)

    async def ping_loop(self):
        print(Exchange.iso8601(Exchange.milliseconds()), 'ping loop')
        pass

    def receive(self):
        raise NotSupported('receive() not implemented')

    def handle_message(self, message):
        raise NotSupported('handle_message() not implemented')

    def closed(self):
        raise NotSupported('closed() not implemented')

    def send(self, message):
        raise NotSupported('send() not implemented')

    def close(self, code=1000):
        raise NotSupported('close() not implemented')

    def create_connection(self, session):
        if True:
            raise NotSupported('create_connection() not implemented')
        return False
