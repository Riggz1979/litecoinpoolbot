import asyncio
import logging
from datetime import datetime

from aiogram import Bot, Dispatcher

from config_reader import config
from handlers import commands, admin, loop_tasks

ADMIN_ID = int(config.admin_id.get_secret_value())


async def say_hi():
    await bot.send_message(ADMIN_ID, f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} '
                                     f'bot online!\nVersion 1.4_rc')


# Bot init
logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher()
dp.startup.register(loop_tasks.price_loop)
dp.startup.register(loop_tasks.watchdog_loop)
dp.startup.register(loop_tasks.alert_loop)
dp.startup.register(say_hi)
dp.include_routers(commands.router, admin.router)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


# Main loop
if __name__ == "__main__":
    asyncio.run(main())
