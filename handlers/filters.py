from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery

from misc.const import admin_ids, moder_ids
from misc.text_of_messages import not_admin, not_moder

class BotAdminMessageFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if flag := (message.from_user.id not in admin_ids):
            await message.answer(not_admin)
        return not flag


class BotAdminCallbackFilter(BaseFilter):
    async def __call__(self, callback: CallbackQuery):
        if flag := (callback.from_user.id not in admin_ids):
            await callback.answer(not_admin)
        return not flag
    
class BotModerMessageFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if flag := (message.from_user.id not in moder_ids):
            await message.answer(not_moder)
        return not flag


class BotModerCallbackFilter(BaseFilter):
    async def __call__(self, callback: CallbackQuery):
        if flag := (callback.from_user.id not in moder_ids):
            await callback.answer(not_moder)
        return not flag