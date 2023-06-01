import logging

from aiogram import Bot, Dispatcher

from handlers import user, admin
from handlers import moderation
from misc.const import token



async def main() -> None:
    bot = Bot(token=token, parse_mode="HTML")
    dp = Dispatcher()

    logging.basicConfig(level=logging.INFO)

    dp.include_routers(user.router, admin.router, moderation.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
