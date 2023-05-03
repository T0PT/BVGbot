from telegram import KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import bot_ui as bui

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Good morning! I could help you in your stressful situation,'+
                             ' trying to find a good way to get to your destination! \n What would you like me to do today?',
                             reply_markup=bui.first_menu_inline)
    dispatcher.remove_handler(first_message_handler)

def greet_me(update, context):
    user = update.message.from_user
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"Hello {user.first_name}!")

def get_location(update, context):
    keyboard = [[KeyboardButton('Send location', request_location=True)]]
    reply_markup = ReplyKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Please send your location",
                             reply_markup=reply_markup)
    
def store_location(update, context):   
    global latitude, longitude  
    latitude = update.message.location.latitude
    longitude = update.message.location.longitude
    keyboard = [[KeyboardButton('Greet me')],
                [KeyboardButton('Send location')],
                [KeyboardButton('Get location')]]
    reply_markup = ReplyKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Got it!",
                             reply_markup=reply_markup)

def send_location(update, context):    
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"Your location is ({latitude}, {longitude})")

latitude, longtitude = 0, 0
updater = Updater(token='YOUR_TOKEN', use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('greet_me', greet_me))
dispatcher.add_handler(MessageHandler(Filters.regex('^Greet me$'), greet_me))
dispatcher.add_handler(MessageHandler(Filters.regex('^Send location$'), get_location))
dispatcher.add_handler(MessageHandler(Filters.regex('^Get location$'), send_location))
dispatcher.add_handler(MessageHandler(Filters.location, store_location))
first_message_handler=MessageHandler(filters= Filters.text, callback= start)
dispatcher.add_handler(first_message_handler)
updater.start_polling(poll_interval=0.5)
updater.idle()
