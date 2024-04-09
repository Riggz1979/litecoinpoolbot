from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

import texts.texts as _texts
from api import pool
from dbwork import sql

data_manager = sql.DBWork('sqlite:///sqlite3.db')
api_work = pool.PoolApi()

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    if data_manager.check_user_exist(message.from_user.id):
        answer = f'Привіт {message.from_user.first_name}!'
    else:
        answer = (f'Привіт {message.from_user.first_name}! '
                  f'Ваш user_id:{message.from_user.id}. API key не зареєстровано')
    await message.answer(answer)


@router.message(Command("stats"))
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


@router.message(Command("api"))
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


@router.message(Command('commands'))
async def commands(message: Message):
    await message.answer(_texts.COMMANDS)


@router.message(Command("watchdog"))
async def set_watchdog(message: Message, command: CommandObject):
    if data_manager.check_user_exist(message.from_user.id):
        if command.args is None:
            await message.answer(f'Watchdog is: {str(data_manager.hash_watchdog(message.from_user.id))} Mh/s')
        elif command.args.isdigit():
            data_manager.hash_watchdog(message.from_user.id, int(command.args))
            await message.answer(f'Watchdog set: {command.args} Mh/s')
        else:
            await message.answer('Wrong arguments')
    else:
        await message.answer('API key не зареєстровано.')