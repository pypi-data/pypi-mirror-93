import logging
import asyncio

log = logging.getLogger('aiotrading')

class MarketStream:

    def __init__(self, exchange, names):
        self.exchange = exchange
        self.names = set(names)
        self.persistent = False
        self.queue = asyncio.Queue()

    async def read(self):
        return await self.queue.get()

    async def write(self, d):
        if d['stream'] in self.names:
            await self.queue.put(d['data'])

    async def open(self):
        await self.exchange.open_market_stream(self)

    async def close(self):
        await self.exchange.close_market_stream(self)
        
    def persist(self):
        self.persistent = True
        
    async def __aenter__(self):
        await self.open()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()
    
    def __str__(self):
        s = ', '.join(self.names)
        p = 's' if len(self.names)>1 else ''
        return f'market data stream{p} {s}'

    def __repr__(self):
        return self.__str__()
