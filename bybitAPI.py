import asyncio
import websockets
import time
import hmac
import hashlib
import binascii
import json

class bybit(api_key: str, secret: str):
    def __init__(self):
        self.secret = secret

    def signature(self, key, message):
        byte_key = binascii.unhexlify(key)
        message = message.encode()
        return hmac.new(byte_key, message, hashlib.sha256).hexdigest().upper()

    async def fetchPrice(self, symbol: str):
        expires = time.now()+1000
        signature = signature(self, self.secret, 'GET/realtime' + expires)
        async with websockets.connect(
                'ws://stream.bybit.com/realtime') as websocket:
            #auth
            await websocket.send(str('{"op":"auth","args":[{' + api_key + '},expires,{' + signature + '}]}'))


            await websocket.send('{"op":"subscribe","args":["instrument.' + symbol + '"]}')
            symbolInfo = await websocket.rcv()
            print('The last price for ' + symbol + ' is ' + str(symbolInfo['data']['last_price']))
            return symbolInfo
    def getPriceInfo(symbol: str)
        symbolInfo = asyncio.get_event_loop().run_until_complete(fetchPrice(self, symbol))

if __name__ == "__main__":
    bybit = bybit(key, secret)
    price = bybit.getPriceInfo('BTCUSD')
