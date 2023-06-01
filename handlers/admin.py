import os
from pathlib import Path
from sys import exit

from aiogram import Router, Bot
from aiogram.filters import Command, Text
from aiogram.types import Message, CallbackQuery

from handlers.filters import BotAdminMessageFilter, BotAdminCallbackFilter
from handlers import keyboards as kb


router = Router()

@router.message(Command(commands=["stop"]), BotAdminMessageFilter())
async def stop(message: Message):
    await message.answer("Bye")
    exit()

