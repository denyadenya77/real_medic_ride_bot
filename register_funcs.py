from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler
from vars_module import *


def register(update, context):
    text = 'Enter user type:'
    buttons = [[
        InlineKeyboardButton(text='DRIVER', callback_data=str(DRIVER)),
        InlineKeyboardButton(text='DOCTOR', callback_data=str(DOCTOR))
    ]]
    keyboard = InlineKeyboardMarkup(buttons)
    update.message.reply_text(text=text, reply_markup=keyboard)
    return GET_USER_STATUS


def get_user_status(update, context):
    user_type = update.callback_query.data

    if user_type is DRIVER:
        user_type = 'driver'
    else:
        user_type = 'doctor'

    text = f'Now you are a {user_type}'
    update.callback_query.answer()
    update.callback_query.edit_message_text(text)
    return ConversationHandler.END
