# keyboards.py
from telebot import types
from config import BUTTONS

def main_menu():
    keyboard = types.ReplyKeyboardMarkup(
        row_width=2,
        resize_keyboard=True,
        one_time_keyboard=False
    )
    
    btn_start = types.KeyboardButton(BUTTONS["start_test"])
    btn_help = types.KeyboardButton(BUTTONS["help"])
    btn_about = types.KeyboardButton(BUTTONS["about"])
    
    keyboard.add(btn_start, btn_help, btn_about)
    return keyboard

def test_keyboard():
    keyboard = types.ReplyKeyboardMarkup(
        row_width=2,
        resize_keyboard=True,
        one_time_keyboard=True
    )
    
    btn_yes = types.KeyboardButton("✅Да")
    btn_no = types.KeyboardButton("❌Нет")
    btn_maybe = types.KeyboardButton("🤔Не знаю")
    btn_back = types.KeyboardButton(BUTTONS["back"])
    
    keyboard.add(btn_yes, btn_no, btn_maybe, btn_back)
    return keyboard

def choice_keyboard(options):
    keyboard = types.ReplyKeyboardMarkup(
        row_width=2,
        resize_keyboard=True,
        one_time_keyboard=True
    )
    
    for option in options:
        keyboard.add(types.KeyboardButton(option))
    
    keyboard.add(types.KeyboardButton(BUTTONS["back"]))
    return keyboard

def result_keyboard():
    keyboard = types.ReplyKeyboardMarkup(
        row_width=2,
        resize_keyboard=True
    )
    
    btn_restart = types.KeyboardButton(BUTTONS["restart_test"])
    btn_help = types.KeyboardButton(BUTTONS["help"])
    
    keyboard.add(btn_restart, btn_help)
    return keyboard

def inline_keyboard_for_professions(professions):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    
    for prof in professions:
        btn = types.InlineKeyboardButton(
            text=prof,
            callback_data=f"prof_{prof}"
        )
        keyboard.add(btn)
    
    return keyboard