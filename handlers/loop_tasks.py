import asyncio

from config_reader import config
from handlers.commands import data_manager, api_work
from api import prices

prices = prices.Prices()
INTERVAL = int(config.interval.get_secret_value())


async def check_watchdogs(bot):
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
        await asyncio.sleep(300)


async def watchdog_loop(bot):
    asyncio.create_task(check_watchdogs(bot))


async def check_alerts_list(bot):
    while True:
        alerts_to_check = data_manager.get_all_alerts()
        for alert in alerts_to_check:
            print(alert)
        print("Alerts")
        await asyncio.sleep(20)


async def alert_loop(bot):
    asyncio.create_task(check_alerts_list(bot))

async def get_prices_loop():
    global price_list
    while True:
        price_list = prices.get_most_popular()
        print(f'Price list: {price_list}, interval: {INTERVAL}')
        await asyncio.sleep(INTERVAL)


async def price_loop():
    asyncio.create_task(get_prices_loop())
