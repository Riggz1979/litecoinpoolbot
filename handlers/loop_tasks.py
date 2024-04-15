import asyncio

import varlist
from api import prices
from config_reader import config
from handlers.commands import data_manager, api_work

prices = prices.Prices()
INTERVAL = int(config.interval.get_secret_value())


async def check_watchdogs(bot):
    """
    Checks if the hash rate is over watchdog value and send message to user if not
    :param bot:
    :return:
    """
    count = 0
    watchdogs = {}
    users_list = []
    while True:
        count += 1
        if count == 1:
            users_list = data_manager.get_all_users()
            for user in users_list:
                watchdogs[user[0]] = 0
        for user in users_list:
            user_id = user[0]
            wd = api_work.get_hash(user[2])  # random.randint(400, 550)
            watchdogs[user_id] += wd
            if count == 5:
                awg_wd = watchdogs[user_id] / count

                if awg_wd < user[3]:
                    await bot.send_message(user[1], f'Warning! Looks like your hash rate low! '
                                                    f'{awg_wd} MH/s vs {user[3]} MH/s')

        if count == 5:
            count = 0
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
            print(user.tg_id)
            alerts_to_check = data_manager.get_user_alerts(user.tg_id)
            for alert in alerts_to_check:
                if alert.go_up is True:
                    if varlist.price_list[alert.crypto] > alert.value:
                        alert_string += f'{alert.crypto} > {alert.value} ({varlist.price_list[alert.crypto]})\n'
                else:
                    if varlist.price_list[alert.crypto] < alert.value:
                        alert_string += f'{alert.crypto} < {alert.value} ({varlist.price_list[alert.crypto]})\n'
            if alert_string != 'Alerts:\n':
                await bot.send_message(user.tg_id, alert_string)
                alert_string = 'Alerts:\n'
        await asyncio.sleep(20)


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
