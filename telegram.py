import asyncio
import json

import aiohttp


class Api(object):
    URL = 'https://api.telegram.org/bot%s/%s'

    def __init__(self, token, loop):
        self._token = token
        self._loop = loop

    async def _request(self, method, message):
        headers = {
            'Content-Type': 'application/json'
        }
        async with aiohttp.ClientSession(loop=self._loop) as session:
            async with session.post(self.URL % (self._token, method),
                                    data=json.dumps(message),
                                    headers=headers) as resp:
                try:
                    assert resp.status == 200
                except:
                    pass

    async def send_message(self, chat_id, text):
        message = {
            'chat_id': chat_id,
            'text': text
        }
        await self._request('sendMessage', message)


class BotHandler(Api):
    def __init__(self, token, loop):
        super().__init__(token, loop)

    async def _handler(self, update):
        print(update)
        await self.send_message(update['message']['chat']['id'],
                                update['message']['text'])

    async def handler(self, request):
        update = await request.json()
        asyncio.ensure_future(self._handler(update))
        return aiohttp.web.Response(status=200)
