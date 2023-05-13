from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import bot_ui as bui
import bot_bvg_requests as bbr

class user(): #user object, being made first time, user messages bot
    def __init__(self, chat_id, name):
        self.chat_id = chat_id
        self.name = name
        self.station = ''
        self.departures = []

def first_start(update, context): #first start
    global users
    chat_id = update.effective_chat.id
    if not update.effective_chat.id in users:
        users[update.effective_chat.id] = user(update.effective_chat.id,  update.message.from_user.first_name)
        bui.first_start_ui(update, context, users[update.effective_chat.id]) #ask for location

def start(update, context): #define user if it is not already, start the bot with greetings
    global users
    register(update, context)
    bui.start_ui(update, context, users[update.effective_chat.id]) #greetme, find transport at location, set periodic checks

def find_departures_at_station(update, context): #check if we already know the station, if not, ask for it
    global users
    register(update, context)
    bui.find_departures_at_station_ui(update, context, users[update.effective_chat.id])

def callback_manager(update, context):
    query = update.callback_query
    if query.data == 'find_departures_at_station':
        find_departures_at_station(update, context)
    query.answer()

def register(update, context):
    global users
    if not update.effective_chat.id in users:
        chat_id = update.effective_chat.id
        users[chat_id] = user(chat_id,  update.message.from_user.first_name)

users={}

updater = Updater(token='', use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('find_departures', find_departures_at_station))
dispatcher.add_handler(CallbackQueryHandler(callback_manager))
dispatcher.add_handler(MessageHandler(first_start))
updater.start_polling(poll_interval=0.5)
updater.idle()