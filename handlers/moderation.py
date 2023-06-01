import os
import shutil
from pathlib import Path

from aiogram import Router, Bot
from aiogram.filters import Command, Text, StateFilter
from aiogram.types import Message, CallbackQuery, PhotoSize, FSInputFile
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


from handlers.filters import BotModerMessageFilter, BotModerCallbackFilter
from handlers import keyboards as kb
from misc.text_of_messages import start_moderation, moderator, moderator_callbacks, finish_moderation, cumback, cancel_moderation

router = Router()

class ModStates(StatesGroup):
    moders_ans = State()


async def send_photo(mes: Message, state: FSMContext):
    moderation_folder = os.listdir("moderation")
    if len(moderation_folder) != 0:
        user_folder = Path("moderation", os.listdir("moderation")[0])
        user_folder_list = os.listdir(user_folder)
        if len(user_folder_list) != 0:
            photo = user_folder_list[0]
            mod_photo = Path(user_folder, photo)
            await mes.answer_photo(FSInputFile(mod_photo), reply_markup=kb.InlineKeyboard(moderator, moderator_callbacks))
            await state.set_state(ModStates.moders_ans)
            await state.update_data(data = {"photo_path": mod_photo, "folder": user_folder})
        else:
            os.rmdir(user_folder)
            await send_photo(mes, state)
    if len(moderation_folder) == 0:
        await mes.answer(finish_moderation, reply_markup=kb.ReplyKeyboard(cumback))



@router.message(Command(commands=["smod"]), StateFilter(None), BotModerMessageFilter())
async def starting(message: Message, state: FSMContext):
    await message.answer(start_moderation)
    await send_photo(message, state)

@router.callback_query(Text(text=moderator_callbacks[0]), StateFilter(ModStates.moders_ans), BotModerCallbackFilter())
@router.callback_query(Text(text=moderator_callbacks[1]), StateFilter(ModStates.moders_ans), BotModerCallbackFilter())
async def like(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id,reply_markup=None)
    data = await state.get_data()
    photo = str(data.get("photo_path"))

    if callback.data == moderator_callbacks[0]:
        shutil.copy(photo, 'simps')

    os.remove(photo)
    await state.clear()
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    await send_photo(callback.message, state)

@router.callback_query(Text(text=moderator_callbacks[2]), StateFilter(ModStates.moders_ans), BotModerCallbackFilter())
async def cleaning(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id,reply_markup=None)
    data = await state.get_data()
    user_folder = str(data.get("folder"))
    shutil.rmtree(user_folder)
    await state.clear()
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    await send_photo(callback.message, state)

@router.callback_query(Text(text=moderator_callbacks[3]), StateFilter(ModStates.moders_ans), BotModerCallbackFilter())
async def cleaning(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id,reply_markup=None)
    await state.clear()
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)    
    await callback.message.answer(cancel_moderation, reply_markup=kb.ReplyKeyboard(cumback))

