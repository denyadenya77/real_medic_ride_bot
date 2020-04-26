from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, \
    ReplyKeyboardRemove
from telegram.ext import ConversationHandler
from vars_module import *
from registration_requests import send_registration_request, send_user_deletion_request


def register(update, context):
    if not len(context.chat_data) or not context.chat_data['authorized']:
        text = 'Оберіть тип профілю:'
        buttons = [[
            InlineKeyboardButton(text='Водій-волонтер', callback_data=str(DRIVER)),
            InlineKeyboardButton(text='Мед. працівник', callback_data=str(DOCTOR))
        ]]
        keyboard = InlineKeyboardMarkup(buttons)
        update.message.reply_text(text=text, reply_markup=keyboard)
        return GET_USER_STATUS
    else:
        text = 'Ви вже авторизовані в системі!\n\n' \
               'Натисніть "ВИДАЛИТИ", якщо хочете видалити всю інформацію про себе та свої маршрути.\n' \
               'Натисніть "ВІДМІНИТИ", щоб відмінити дію.\n\n' \
               'БУДЬТЕ ОБЕРЕЖНІ! Видалееі дані неможливо відновити!'
        buttons = [[
            InlineKeyboardButton(text='ВИДАЛИТИ', callback_data=str(DELETE_DATA)),
            InlineKeyboardButton(text='ВІДМІНИТИ', callback_data=str(STOP_ACTION))
        ]]
        keyboard = InlineKeyboardMarkup(buttons)
        update.message.reply_text(text=text, reply_markup=keyboard)
        return CHOSE_DELETE_USER_DATA


def get_user_status(update, context):
    user_type = update.callback_query.data

    if user_type is DRIVER:
        user_type = 'driver'
    else:
        user_type = 'doctor'

    context.user_data['user_type'] = user_type

    text = f'Тепер ви наш {user_type}!'
    update.callback_query.answer()
    update.callback_query.edit_message_text(text)

    contact_keyboard = KeyboardButton('Відправити номер телефону', request_contact=True)
    custom_keyboard = [[contact_keyboard]]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True, one_time_keyboard=True)
    context.bot.send_message(update.effective_message.chat_id,
                             f'Натисніть копку, аби зазначити номер телефону.',
                             reply_markup=reply_markup)

    return GET_USER_CONTACT


def get_user_phone_and_name(update, context):
    contact = update.effective_message.contact
    first_name = contact.first_name
    last_name = contact.last_name
    phone = contact.phone_number
    user_type = context.user_data['user_type']
    user_telegram_id = update.effective_user.id

    # сохраняем контакт юзера, чтобы в adding_rides_funcs отправлять его водителю
    context.chat_data['user_contact'] = contact

    response = send_registration_request(telegram_id=user_telegram_id,
                                         user_type=user_type,
                                         first_name=first_name,
                                         last_name=last_name,
                                         phone_number=phone)

    if response.status_code == 201:
        context.chat_data['authorized'] = True
        update.effective_message.reply_text(f'Вітаємо! Тепер ви зарєєстровні у системі!',
                                            reply_markup=ReplyKeyboardRemove())
    else:
        update.effective_message.reply_text('Случилась какая-то ошибка. Попробуйте еще раз.',
                                            reply_markup=ReplyKeyboardRemove())
    context.user_data.clear()
    return ConversationHandler.END


def delete_or_stop(update, context):
    action = update.callback_query.data

    if action is DELETE_DATA:

        response = send_user_deletion_request(telegram_id=update.effective_user.id)

        if response.status_code == 200:
            text = 'Ваші дані видалено з системи.\n' \
                   'Ви можете зареєстнуватися знову обрав команду /register'
            context.chat_data['authorized'] = False
        else:
            text = 'Случилась какая-то ошибка. Попробуйте еще раз.'
    else:
        text = 'Дякуємо, що залилаєтесь з нами!'

    update.callback_query.answer()
    update.callback_query.edit_message_text(text)

    return ConversationHandler.END
