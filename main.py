import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters.command import Command, CommandObject
from aiogram.types import Message

import texts.texts as _texts
from api import pool, prices
from config_reader import config
from dbwork import sql

api_work = pool.PoolApi()
prices = prices.Prices()
data_manager = sql.DBWork('sqlite:///sqlite3.db')

INTERVAL = int(config.interval.get_secret_value())
price_list = {}
users = data_manager.get_all_users()


async def get_prices_loop():
    global price_list
    while True:
        price_list = prices.get_most_popular()
        print(f'Price list: {price_list}, interval: {INTERVAL}')
        await asyncio.sleep(INTERVAL)


async def work_loop():
    asyncio.create_task(get_prices_loop())


# Bot init
logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher()
dp.startup.register(work_loop)


@dp.message(Command("start"))
async def cmd_start(message: Message):
    if data_manager.check_user_exist(message.from_user.id):
        answer = f'Привіт {message.from_user.first_name}!'
    else:
        answer = (f'Привіт {message.from_user.first_name}! '
                  f'Ваш user_id:{message.from_user.id}. API key не зареєстровано')
    await message.answer(answer)


@dp.message(Command("api"))
async def cmd_api(message: Message, command: CommandObject):
    if command.args is None:
        await message.answer(
            "Формат команди: /api 'ваш ключ'"
        )
    else:
        key = command.args
        if api_work.check_key(key) and not data_manager.check_api_key_exist(key):

            data_manager.add_user(message.from_user.id, key)
            await message.answer('Ключ успішно зареєстровано.')
        else:
            await message.answer('Невірний ключ API, або вже зареєстровано.')


@dp.message(Command("stats"))
async def cmd_get_stats(message: Message):
    if data_manager.check_user_exist(message.from_user.id):
        api_key = data_manager.get_user(message.from_user.id).api_key
        response = api_work.get_stats(api_key)
        hash_rate = response['user']['hash_rate']
        ltc_bal = response['user']['unpaid_rewards']
        doge_bal = response['user']['unpaid_rewards_doge']
        app_ltc = response['user']['expected_24h_rewards']
        app_doge = response['user']['expected_24h_rewards_doge']
        app_usd = float(response['market']['ltc_usd']) * app_ltc + float(
            response['market']['doge_usd']) * app_doge
        await message.answer(f'Hash rate: {hash_rate // 1000}Mh\n'
                             f'LTC balance: {ltc_bal}\n'
                             f'Doge balance: {doge_bal}\n'
                             f'24h LTC: {app_ltc}\n'
                             f'24h DOGE: {app_doge}\n'
                             f'24h USD: {app_usd}'
                             )
    else:
        await message.answer('API key не зареєстровано')


@dp.message(Command('prices'))
async def popular_prices(message: Message):
    await message.answer(f'Bitcoin:      {price_list['bitcoin']} USD\n'
                         f'Litecoin:    {price_list['litecoin']} USD\n'
                         f'Doge:         {price_list['dogecoin']} USD\n'
                         f'Ethereum:  {price_list['ethereum']} USD')


@dp.message(Command('commands'))
async def commands(message: Message):
    await message.answer(_texts.COMMANDS)


async def main():
    await dp.start_polling(bot)


# Main loop
if __name__ == "__main__":
    asyncio.run(main())
