import os
import random
import shutil

from pathlib import Path

from aiogram import Bot, Router, F

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, Text, StateFilter
from aiogram.types import Message, PhotoSize, CallbackQuery, FSInputFile


from handlers import keyboards as kb
from handlers.filters import BotAdminMessageFilter
from misc.text_of_messages import welcome_mes, first_ask, opps_mes, opps, opps_callbacks, pics_is_over, girl_opps, girl_stop, cumback, cleaning, enjoy, we_wait, comment_snd, oxygen, mes_for_admin, smth_new, wait_for_moderation, lonelyness
from misc.paths_for_messages import welcome_gif, opps_gif, oxygen_path
from misc.const import admin_ids

router = Router()
messages_dates = []

'''
Состояния
'''

class BotState(StatesGroup):
    waiting_comment = State()
    waiting_photo = State()


'''
Функции
'''

@router.message(Command(commands=["start","help"]), StateFilter(None))
async def welcome_command(message: Message, state: FSMContext):
    if os.path.isdir(Path("users", str(message.chat.id))) == False:
        os.mkdir(Path("users", str(message.chat.id)))
    await message.answer(welcome_mes, reply_markup=kb.ReplyKeyboard([first_ask]))
    await message.answer_animation(FSInputFile(welcome_gif))

@router.message(Text(text = first_ask), StateFilter("*"))
@router.message(Command(commands=["opps"]))
async def opportunities(message: Message, state: FSMContext):
    await state.clear()
    await message.answer_animation(opps_gif, reply_markup=kb.DeleteMarkup())
    await message.answer(opps_mes, reply_markup=kb.InlineKeyboard(opps, opps_callbacks))


'''
Работа с папкой simps
'''

async def send_pic(mes: Message):
    id = mes.chat.id

    name_of_pic = str(random.choice(os.listdir('simps/')))
    user_folder = Path("users/" , str(id))
    pic_max = (len(os.listdir('simps/')) != len(os.listdir(user_folder)))
    flag = id in admin_ids
    while os.path.isfile(Path(user_folder, name_of_pic)) == True and pic_max:
        name_of_pic = str(random.choice(os.listdir('simps/')))
    pic = FSInputFile(Path('simps', name_of_pic))
    if pic_max:
        await mes.answer_photo(pic, protect_content=not(flag), reply_markup=kb.ReplyKeyboard(girl_opps))
        shutil.copyfile(Path('simps', name_of_pic),Path(user_folder, name_of_pic))
    else:
        await mes.answer(pics_is_over)


@router.callback_query(Text(text = opps_callbacks[0]), StateFilter(None))
async def girls(callback: CallbackQuery, bot: Bot):
    await bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id,reply_markup=None)
    await callback.message.answer(enjoy)
    await send_pic(callback.message)

@router.message(Text(text = girl_opps[0]), StateFilter(None))
async def circle(message: Message):
    await send_pic(message)

    
@router.message(Text(text = girl_opps[1]), StateFilter(None))
async def opportunities(message: Message):
    await message.answer(girl_stop, reply_markup=kb.ReplyKeyboard(cumback))


@router.message(Command(commands=['clear']), StateFilter(None))
async def tidy(message: Message):
    user_folder = Path('users', str(message.chat.id))
    shutil.rmtree(user_folder)
    os.mkdir(user_folder)
    await message.answer(cleaning)
    
'''
Комментарии
'''

@router.callback_query(Text(text = opps_callbacks[2]), StateFilter(None))
async def comment_waiting(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id,reply_markup=None)
    await callback.message.answer(we_wait)
    await state.set_state(BotState.waiting_comment)


    
@router.message(BotState.waiting_comment)
async def comment_sending(message: Message, bot: Bot, state: FSMContext):
    await state.clear()
    for admin in admin_ids:
        await bot.send_message(chat_id=admin, text = mes_for_admin.format(message.from_user.first_name,message.from_user.username) +  message.text )
    await message.answer(comment_snd, reply_markup=kb.ReplyKeyboard(cumback))



'''
Интерфейс добавления фото
'''

@router.callback_query(Text(text = opps_callbacks[1]), StateFilter(None))
async def photo_waiting(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id,reply_markup=None)
    await callback.message.answer(smth_new)
    await state.set_state(BotState.waiting_photo)

@router.message(BotState.waiting_photo)
async def process_photo(message: Message, bot: Bot, state: FSMContext):
    date = message.date
    if (message.chat.id, date) not in messages_dates:
        messages_dates.append((message.chat.id, date))
        await message.answer(wait_for_moderation, reply_markup=kb.ReplyKeyboard(cumback))
    await state.clear()
    
    if os.path.isdir(Path("moderation", str(message.chat.id))) == False:
        os.mkdir(Path("moderation", str(message.chat.id)))
    moderation_folder = Path("moderation", str(message.chat.id))
    photo = message.photo.pop()
    photo_path = Path(moderation_folder, f"{photo.file_id}.jpg")
    await bot.download(photo, photo_path)
    
        
