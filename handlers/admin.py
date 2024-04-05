import os
import sys

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from config_reader import config

ADMIN_ID = int(config.admin_id.get_secret_value())
router = Router()


def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)


@router.message(Command('admin'))
async def admin(message: Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer('Yes')


@router.message(Command('restart'))
async def restart(message: Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer("Restarting...")
        restart_program()
