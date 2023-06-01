from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

def InlineKeyboard(buttons, callbacks):
    return InlineKeyboardMarkup(inline_keyboard= [[InlineKeyboardButton(text = buttons[i], callback_data=callbacks[i]) for i in range(len(buttons))]], row_width = 3)

def ReplyKeyboard(buttons):
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text = buttons[i]) for i in range (len(buttons))]], resize_keyboard=True, one_time_keyboard=True)

def DeleteMarkup():
    return ReplyKeyboardRemove()
