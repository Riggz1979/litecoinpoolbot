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
        await message.answer('Yes, you are admin!')
    else:
        await message.answer('You don\'t have admin permissions')


@router.message(Command('restart'))
async def restart(message: Message, dispatcher):
    if message.from_user.id == ADMIN_ID:
        await message.answer("Restarting...")
        await dispatcher.stop_polling()
        restart_program()


@router.message(F.document)
async def ota(message: Message, bot, dispatcher):
    if message.from_user.id == ADMIN_ID and message.document.file_name == 'OTA.zip':
        if os.path.exists(f'{PATH}/OTA.zip'):
            os.remove('OTA.zip')
            await message.answer('Old OTA zip file deleted')
        else:
            await message.answer('Old OTA zip file not found')

        await message.answer('Downloading...')
        await bot.download(message.document, destination=f'{PATH}/{message.document.file_name}')

        with zipfile.ZipFile(message.document.file_name, mode='r') as ota_file:
            ota_file.extractall(PATH)

        await message.answer('OTA received\nRestarting program')
        await dispatcher.stop_polling()
        restart_program()
