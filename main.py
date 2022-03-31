from aiohttp import web

from telegram import BotHandler


app = web.Application()
app.add_routes([web.get('/', BotHandler.handler)])

if __name__ == '__main__':
    web.run_app(app)
