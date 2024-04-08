import os
import sys
import zipfile

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message


from config_reader import config

ADMIN_ID = int(config.admin_id.get_secret_value())
router = Router()

PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)


@router.message(Command('admin'))
async def admin(message: Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer(PATH)


@router.message(Command('restart'))
async def restart(message: Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer("Restarting...")
        restart_program()


@router.message(F.document)
async def download(message: Message):
    if message.from_user.id == ADMIN_ID:
        if message.document.file_name == 'OTA.zip':
            with zipfile.ZipFile(message.document.file_name, mode='r') as ota:
                print(ota.namelist())
                ota.extractall(PATH)

            await message.answer('OTA received')
            restart_program()
