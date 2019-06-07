import asyncio
import websockets
import time
import hmac
import hashlib
import binascii
import json

api_key = ""
secret = ""
expires = time.now()+1000
signature = create_sha256_signature(secret, 'GET/realtime' + expires)
symbol = 'BTCUSD'

def create_sha256_signature(key, message):
    byte_key = binascii.unhexlify(key)
    message = message.encode()
    return hmac.new(byte_key, message, hashlib.sha256).hexdigest().upper()

async def fetchPrice():
    async with websockets.connect(
            'ws://stream.bybit.com/realtime') as websocket:
        #auth
        await websocket.send(str('{"op":"auth","args":[{' + api_key + '},expires,{' + signature + '}]}'))
        

        await websocket.send('{"op":"subscribe","args":["instrument.' + symbol + '"]}')
        symbolInfo = await websocket.rcv()
        print('The last price for ' + symbol + ' is ' + str(symbolInfo['data']['last_price']))

asyncio.get_event_loop().run_until_complete(fetchPrice())
