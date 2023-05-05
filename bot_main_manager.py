from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import bot_ui as bui

def start(update, context): #first being called if any text message is sent, after that only if command '/start' is sent   
    global user
    user=update.message.from_user
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Good morning! I could help you in your stressful situation,'+
                             ' trying to find a good way to get to your destination! \n What would you like me to do today?',
                             reply_markup=bui.start_inline)
    # update.message.reply_text('Please choose:', reply_markup=bui.first_menu_inline)
    # dispatcher.remove_handler(first_message_handler)

def greet_me(update, context): #test func 
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"Hello {user.first_name}! \n")

def get_location(update, context): #sends user a button, which sends his location
    keyboard = [[KeyboardButton('Send location', request_location=True)]]
    reply_markup = ReplyKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Please send your location",
                             reply_markup=reply_markup)
    
def find_station_fromlocation(update, context):   #when recieved location, stores it
    global recieving_station, latitude, longitude, user_station
    if recieving_station==True: 
        latitude = update.message.location.latitude
        longitude = update.message.location.longitude
        #ask BVG for station
        user_station='S+U Alexanderplatz'
        recieving_station=False
        if departures_to_send:send_departures(update, context)
    else:        
        latitude = update.message.location.latitude
        longitude = update.message.location.longitude

def find_station_frommessage(update, context): #when recieved station, stores it
    global recieving_station, latitude, longitude, user_station, departures_to_send
    #ask BVG for station
    print('trying to find')
    latitude = 52.520751
    longitude = 13.411683
    user_station='S+U Alexanderplatz' 
    recieving_station=False
    if departures_to_send:send_departures(update, context)

def send_departures(update, context): #send_departures from defined station, if not defined, is to be defined
    global departures_to_send
    departures_to_send=True
    if user_station != '':
            #ask BVG for departures
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text='Here are the departures from your station: \n'+
                                    10*('    '+'at '+'   '+'to '+'    '+'platform '+'    '+'\n'),
                                    reply_markup=bui.stations_list_ask_get_new)
            departures_to_send=False
    else:
        #write, that there is no station defined, so it has to be defined
        #give two options to find it, by its name or by its coordinates
        print('no station defined, asking user')
        define_station(update, context)

def define_station(update, context): #station to be defined
    global recieving_station
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Please, define station, from which you want to get departures information, '+
                             'you can either send it\'s name or its coordinates',
                             reply_markup=bui.ask_location,)
    recieving_station=True

def set_periodic_departures_checks(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='This function does not work yet, sorry :(\nStay tuned!')

def callback_manager(update, context): #callback manager, to be called when user clicks on inline button
    global departures_to_send
    query = update.callback_query
    if query.data == 'greet_me':
        greet_me(update, context)
    elif query.data == 'send_departures':
        send_departures(update, context)
    elif query.data == 'check_at_another':
        define_station(update, context)
        departures_to_send=True
    elif query.data == 'set_periodic_departures_checks':
        set_periodic_departures_checks(update, context)
    query.answer()

def message_filter(update, context): #is supposed to work every time text message, which does not contain command or location, is sent 
    global first_question, recieving_station
    if first_question:
        start(update, context)
        first_question=False
    elif recieving_station:
        find_station_frommessage(update, context)

def send_location(update, context): #sends his own location, beeing called at request
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"Your location is ({latitude}, {longitude})")
    
latitude, longtitude = 0, 0
recieving_station=False
first_question=True
departures_to_send=False
user_station='' # user_station='S+U Alexanderplatz' #name or id 900100026 , i dont know yet what is needed
updater = Updater(token='YOUR_TOKEN', use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('greet_me', greet_me))
dispatcher.add_handler(CommandHandler('get_location', send_location))
dispatcher.add_handler(MessageHandler(Filters.regex('^Greet me$'), greet_me))
dispatcher.add_handler(MessageHandler(Filters.regex('^Send location$'), get_location))
dispatcher.add_handler(MessageHandler(Filters.location, find_station_fromlocation))
dispatcher.add_handler(MessageHandler(Filters.text, message_filter))
dispatcher.add_handler(CallbackQueryHandler(callback_manager))
updater.start_polling(poll_interval=0.5)
updater.idle()