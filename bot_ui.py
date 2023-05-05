from typing import Any
from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
# from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

first_menu = ReplyKeyboardMarkup([[KeyboardButton('Greet me')],
                    [KeyboardButton('Find nearest transport on the station')],
                    [KeyboardButton('Set periodic transport checks')]], one_time_keyboard=True)


start_inline = InlineKeyboardMarkup([[InlineKeyboardButton(text='Greet me', url='https://www.youtube.com/watch?v=xvFZjo5PgG0')],
                    [InlineKeyboardButton(text='Find available transport departures', callback_data='send_departures')],
                    [InlineKeyboardButton(text='Set periodic departures checks', callback_data='set_periodic_departures_checks')]],) #this is not done yet

ask_location = ReplyKeyboardMarkup([[KeyboardButton('Send location', request_location=True)]], one_time_keyboard=True)

stations_list_ask_get_new=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Check at another station', callback_data='check_at_another')]])