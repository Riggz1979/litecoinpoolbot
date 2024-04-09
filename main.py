import asyncio
import logging
from datetime import datetime

from aiogram import Bot, Dispatcher
from aiogram.filters.command import Command
from aiogram.types import Message

from api import prices
from config_reader import config
from handlers import commands, admin

prices = prices.Prices()

INTERVAL = int(config.interval.get_secret_value())
ADMIN_ID = int(config.admin_id.get_secret_value())
price_list = {}


async def say_hi():
    await bot.send_message(ADMIN_ID, f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} '
                                     f'bot online!\nVersion 1.1')


async def get_prices_loop():
    global price_list
    while True:
        price_list = prices.get_most_popular()
        print(f'Price list: {price_list}, interval: {INTERVAL}')
        await asyncio.sleep(INTERVAL)


async def price_loop():
    asyncio.create_task(get_prices_loop())


# Bot init
logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher()
dp.startup.register(price_loop)
dp.startup.register(say_hi)
dp.include_routers(commands.router, admin.router)


@dp.message(Command('prices'))
async def popular_prices(message: Message):
    await message.answer(f'Bitcoin:      {price_list['bitcoin']} USD\n'
                         f'Litecoin:    {price_list['litecoin']} USD\n'
                         f'Doge:         {price_list['dogecoin']} USD\n'
                         f'Ethereum:  {price_list['ethereum']} USD')


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


# Main loop
if __name__ == "__main__":
    asyncio.run(main())
