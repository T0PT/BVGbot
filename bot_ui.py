from typing import Any
from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

first_menu = ReplyKeyboardMarkup([[KeyboardButton('Greet me')],
                    [KeyboardButton('Find nearest transport on the station')],
                    [KeyboardButton('Set periodic transport checks')]], one_time_keyboard=True)


first_menu_inline = InlineKeyboardMarkup([[InlineKeyboardButton(text='Greet me', callback_data='/greet_me')],
                    [InlineKeyboardButton(text='Find nearest transport on the station', callback_data='/greet_me')],
                    [InlineKeyboardButton(text='Set periodic transport checks', callback_data='/greet_me')]])