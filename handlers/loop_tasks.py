import asyncio
from random import randint

import varlist
from api import prices
from config_reader import config
from handlers.commands import data_manager, api_work

prices = prices.Prices()
INTERVAL = int(config.interval.get_secret_value())
TEST = config.test.get_secret_value() == 'True'


async def check_watchdogs(bot):
    """
    Checks if the hash rate is over watchdog value and send message to user if not
    :param bot:
    :return:
    """
    count = 0
    # dict for watchdogs
    watchdogs = {}
    # list for users
    users_list = []
    while True:
        count += 1
        if count == 1:
            users_list = data_manager.get_all_users()
            for user in users_list:
                watchdogs[user.id] = 0
        for user in users_list:
            user_id = user.id
            if TEST:
                hash_rate = randint(400, 550)  # random value for test mode
                print(f'Emulated hash rate:{hash_rate}')
            else:
                hash_rate = api_work.get_hash(user.api_key)
                print(f'API hash rate:{hash_rate}')
            watchdogs[user_id] += hash_rate
            if count == 5:
                awg_wd = watchdogs[user_id] / count
                if awg_wd < user.hash_wd:
                    await bot.send_message(user.tg_id, f'Warning!\n'
                                                       f'Looks like your hash rate low!\n'
                                                       f'{int(awg_wd)} MH/s < {user.hash_wd} MH/s')
        if count == 5:
            count = 0
        if TEST:
            await asyncio.sleep(10)
        else:
            await asyncio.sleep(360)


async def check_alerts_list(bot):
    """
    Checking alerts list and sending message to users
    :param bot:
    :return:
    """
    while True:
        alert_string = 'Alerts:\n'
        users_list = data_manager.get_all_users()
        for user in users_list:
            alerts_to_check = data_manager.get_user_alerts(user.tg_id)
            for alert in alerts_to_check:
                if alert.go_up is True:
                    if varlist.price_list[alert.crypto] > alert.value:
                        alert_string += (f'{alert.id}: '
                                         f'{alert.crypto} > '
                                         f'{alert.value} ('
                                         f'{varlist.price_list[alert.crypto]}'
                                         f')\n')
                else:
                    if varlist.price_list[alert.crypto] < alert.value:
                        alert_string += (f'{alert.id}: '
                                         f'{alert.crypto} < '
                                         f'{alert.value} ('
                                         f'{varlist.price_list[alert.crypto]}'
                                         f')\n')
            if alert_string != 'Alerts:\n':
                await bot.send_message(user.tg_id, alert_string)
                alert_string = 'Alerts:\n'
        if TEST:
            await asyncio.sleep(30)
        else:
            await asyncio.sleep(INTERVAL)


async def get_prices_loop():
    """
    Get prices of crypto from coingecko
    Saving prices in varlist.price_list
    :return:
    """
    while True:
        varlist.price_list = prices.get_most_popular()
        await asyncio.sleep(INTERVAL)


async def alert_loop(bot):
    asyncio.create_task(check_alerts_list(bot))


async def price_loop():
    asyncio.create_task(get_prices_loop())


async def watchdog_loop(bot):
    asyncio.create_task(check_watchdogs(bot))
