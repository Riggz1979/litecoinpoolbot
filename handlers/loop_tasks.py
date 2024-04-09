import asyncio
import random

from handlers.commands import data_manager


# TODO: Need to finish and optimize
async def check_watchdogs(bot):
    count = 0
    watchdogs = {}
    watchdogs[1] = 0
    watchdogs[2] = 0
    while True:
        count += 1
        users_list = data_manager.get_all_users()
        print(f'Count: {count}')
        for user in users_list:
            print(user)
            user_id = user[0]
            wd = random.randint(400, 550)  # api_work.get_hash(user[2])
            watchdogs[user_id] += wd
            if count == 10:
                awg_wd = watchdogs[user_id] / count
                print(awg_wd)
                if awg_wd < user[3]:
                    await bot.send_message(user[1], 'wd')

        if count == 10:
            count = 0
            watchdogs[1] = 0
            watchdogs[2] = 0

        await asyncio.sleep(120)


# END TODO

async def watchdog_loop(bot):
    asyncio.create_task(check_watchdogs(bot))
