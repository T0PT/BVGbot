# from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
import bot_ui as bui
import bot_bvg_requests as bbr

class user(): #user object, being made first time, user messages bot
    def __init__(self, chat_id, name):
        self.chat_id = chat_id
        self.name = name
        self.station = ''
        self.recieving_station=False
        self.departures = []
    
    def handle_message(self, update, context):
        text = update.message.text
        if text == '/start':
            bui.start_ui(update, context)
            self.recieving_station=False
        elif text == '/greet_me':
            bui.greet_me_trap_ui(update, context) 
            self.recieving_station=False
        elif self.recieving_station: #if user is asking for stations
            self.station_names, self.station_ids, error = bbr.find_station_from_name(name=update.message.text)
            bui.ask_for_answer(update=update, context=context, options=self.station_names, no_correct_answer_text='Check at another location', 
                               message_text='Pick your station, please')
            print('ask bvg for station: ' +self.station)
            self.recieving_station=False
            self.recieving_station_options=True
        else:
            self.first_time(update, context)

    def handle_callback(self, update, context):
        query = update.callback_query
        if query.data == 'send_departures':
            self.send_departures(update, context)
        elif query.data == 'set_periodic_departures_checks':
            bui.apologize_ui(update, context)
        elif query.data in ['0 option','1 option','2 option','3 option','4 option','no_correct_answer']:
            self.pick_option(update, context)
        elif query.data=='forget_station':
            self.station = ''
            self.send_departures(update, context)
        query.answer()

    def handle_location(self, update, context):
        if self.recieving_station:
            latitude = update.message.location.latitude
            longitude = update.message.location.longitude    
            print('ask bvg for station: ' + str(latitude) + ' ' + str(longitude)) #ask bvg for station
            self.station_names, self.station_ids, error = bbr.find_station_from_coordinates(latitude, longitude)
            print(error)
            if error==False:
                bui.ask_for_answer(update=update, context=context, options=self.station_names, no_correct_answer_text='Check at another location', 
                                message_text='Pick your station, please')
                self.recieving_station=False
                self.recieving_station_options=True
            else:
                bui.throw_error(update=update, context=context, message_text='Unfortunately, there was an error on our side, sorry about that, you could try agian a bit later')
                self.recieving_station=False
                self.recieving_station_options=True
            
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    
    def first_time(self, update, context):
        bui.start_ui(update, context)

    def pick_option(self, update, context):
        if self.recieving_station_options:
            data=update.callback_query.data
            print(data)
            if data == 'no_correct_answer':
                self.define_station(self, update, context)
            else:
                number=int(data[0])
                self.station=self.station_ids[int(number)]
                print(self.station)
                self.send_departures(update, context)
            self.recieving_station_options=False

    def send_departures(self, update, context):
        if self.station == '':
            self.define_station(update, context)
        else:
            line_names, times, directions, platforms, error = bbr.get_departures_from_station(self.station, results=100)
            print(error)
            text_to_send=''
            for i in range(len(line_names)):
                text_to_send += str(line_names[i])+' to '+ str(directions[i]) + ' at ' + str(times[i][11:16]) + ' from ' + str(platforms[i]) + ' platform \n'
            # print(type(text_to_send))
            bui.send_departures(update, context, text_to_send)            
                #CONTINUE HERE!!!!!

    def define_station(self, update, context):
        bui.station_ask_ui(update, context)
        self.recieving_station=True

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def message_manager(update, context):
    global users
    chat_id = update.message.chat_id
    if chat_id not in users: #check if user not exists        
        users[chat_id] = user(chat_id, update.message.from_user.first_name)
    users[chat_id].handle_message(update, context)  #make user obj do what is needed  

def callback_manager(update, context):
    global users
    chat_id = update.callback_query.message.chat_id
    if chat_id not in users: #check if user not exists        
        users[chat_id] = user(chat_id, update.callback_query.message.from_user.first_name)
    users[chat_id].handle_callback(update, context) #make user obj do what is needed 

def location_manager(update, context):
    global users
    chat_id = update.message.chat_id
    if chat_id not in users: #check if user not exists        
        users[chat_id] = user(chat_id, update.message.from_user.first_name)
    users[chat_id].handle_location(update, context) #make user obj do what is needed 

users={}

updater = Updater(token='', use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(MessageHandler(filters=Filters.text, callback=message_manager))
dispatcher.add_handler(MessageHandler(filters=Filters.location, callback=location_manager))
dispatcher.add_handler(CallbackQueryHandler(callback=callback_manager))
updater.start_polling()
updater.idle()