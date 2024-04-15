from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

import texts.texts as _texts
import varlist
from api import pool
from config_reader import config
from dbwork import sql

DATABASE = config.database.get_secret_value()
data_manager = sql.DBWork(DATABASE)
api_work = pool.PoolApi()

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    if data_manager.check_user_exist(message.from_user.id):
        answer = f'Hi, {message.from_user.first_name}! Ready to work'
    else:
        answer = (f'Hi, {message.from_user.first_name}! '
                  f'Your tg_id:{message.from_user.id}. API key not registered')
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
        await message.answer('API key not registered')


@router.message(Command('prices'))
async def popular_prices(message: Message):
    await message.answer(f'Bitcoin:      {varlist.price_list['bitcoin']} USD\n'
                         f'Litecoin:    {varlist.price_list['litecoin']} USD\n'
                         f'Doge:         {varlist.price_list['dogecoin']} USD\n'
                         f'Ethereum:  {varlist.price_list['ethereum']} USD')


@router.message(Command("api"))
async def cmd_api(message: Message, command: CommandObject):
    if command.args is None:
        await message.answer(
            "Command format: /api 'your_key'"
        )
    else:
        key = command.args
        if api_work.check_key(key) and not data_manager.check_api_key_exist(key):

            data_manager.add_user(message.from_user.id, key)
            await message.answer('API key successfully added.')
        else:
            await message.answer('Wrong API key, or API key already registered.')


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
        await message.answer('API key not registered.')


@router.message(Command("set_alert"))
async def set_alert(message: Message, command: CommandObject):
    if command.args is None:
        await message.answer(
            'No arguments provided'
        )
        return
    try:
        crypto, gt, val = command.args.split(" ", maxsplit=2)
    except ValueError:
        await message.answer(
            'Wrong arguments. Please try again.'
        )
        return
    if crypto not in ['bitcoin', 'litecoin', 'dogecoin', 'ethereum']:
        await message.answer('Unsupported crypto type.')
        return None
    if gt == '>':
        gt_add = True
    elif gt == '<':
        gt_add = False
    else:
        await message.answer('Alert must be > <')
        return None
    if len(val) < 12:
        try:
            val = float(val)
            print(val)
        except ValueError:
            await message.answer('Check value!')
            return None
        data_manager.set_alert(message.from_user.id, crypto.lower(), val, gt_add)
        await message.answer(f'Alert set: {crypto}{gt}{val}')
    else:
        await message.answer('Check value!')


@router.message(Command('alerts'))
async def alerts_list(message: Message):
    answer_str = f'{message.from_user.first_name} alerts list:\n'
    alerts = data_manager.alerts_list(message.from_user.id)
    for alert in alerts:
        if alert.go_up:
            ans_go_up = '>'
        else:
            ans_go_up = '<'
        answer_str += (f'{alert.id}: '
                       f'{alert.crypto}'
                       f'{ans_go_up}'
                       f'{alert.value}\n')
    await message.answer(answer_str)


@router.message(Command('del_alert'))
async def del_alert(message: Message, command: CommandObject):
    if command.args is None:
        await message.answer(
            'No arguments provided'
        )
        return
    if command.args.isdigit():
        if data_manager.delete_alert(message.from_user.id, int(command.args)):
            await message.answer('Alert deleted!')
        else:
            await message.answer('Invalid alert id!')
