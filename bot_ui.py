from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
# from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

def start_ui(update, context):
    start_inline = InlineKeyboardMarkup([[InlineKeyboardButton(text='Greet me', url='https://www.youtube.com/watch?v=xvFZjo5PgG0')],
                    [InlineKeyboardButton(text='Find available transport departures', callback_data='send_departures')],
                    [InlineKeyboardButton(text='Set periodic departures checks', callback_data='set_periodic_departures_checks')]],) #this is not done yet
    context.bot.send_message(chat_id=update.effective_chat.id, text='Good morning! I could help you in your stressful situation,'+
                             ' trying to find a good way to get to your destination! \n What would you like me to do today?',
                             reply_markup=start_inline)
    
def greet_me_trap_ui(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Hi! I am glad to see you! I found an interesting video for you!',
                             reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text='Show me', url='https://www.youtube.com/watch?v=xvFZjo5PgG0')]]))

def station_ask_ui(update, context):
    ask_location = ReplyKeyboardMarkup([[KeyboardButton('Send location', request_location=True)]], one_time_keyboard=True)
    context.bot.send_message(chat_id=update.effective_chat.id, text='Please, define station, from which you want to get departures information, '+
                             'you can either send it\'s name or its coordinates',
                             reply_markup=ask_location)
    
def apologize_ui(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Sorry, this feature is not done yet')

stations_list_ask_get_new=InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Check at another station', callback_data='check_at_another')]])

def send(update, context, text):
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)

def send_departures(update, context, text):
    context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text='Check at another', callback_data='forget_station')]]))

def ask_for_answer(update, context, options=['1','2','3','4'], no_correct_answer_butt=True, no_correct_answer_text='No correct answer',
                    callback_from=0, message_text='Pick one option, please'):
    buttons=[InlineKeyboardButton(text=option, callback_data=str(i+callback_from)+' option') for i, option in enumerate(options)]
    if no_correct_answer_butt:
        buttons.append(InlineKeyboardButton(text=no_correct_answer_text, callback_data='no_correct_answer'))
    keyboard= InlineKeyboardMarkup([[button] for button in buttons])
    context.bot.send_message(chat_id=update.effective_chat.id, text=message_text,
                             reply_markup=keyboard)