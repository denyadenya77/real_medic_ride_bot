from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Location
from telegram.ext import ConversationHandler
from vars_module import *
import logging

logging.basicConfig(level=logging.DEBUG)


def add_ride(update, context):
    keyboard = [[InlineKeyboardButton("Однократна поїздка", callback_data=str(ONE_TIME))],
                [InlineKeyboardButton("Регулярна поїздка", callback_data=str(REGULAR))]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Якщо ви здійснюєте цю поїздку регулярно - повідомте про це, будь ласка.',
                              reply_markup=reply_markup)
    return GET_RIDE_STATUS


def get_ride_status_and_user_id(update, context):
    query = update.callback_query
    ride_type = query.data

    if ride_type is ONE_TIME:
        context.user_data['ride_type'] = 'ONE_TIME'
        text = 'Введіть час відправлення у форматі HH.MM:'
    else:
        context.user_data['ride_type'] = 'REGULAR'
        text = 'Надішліть координати старту. \n51.6680, 32.6546'

    update.callback_query.answer()
    update.callback_query.edit_message_text(f'Тип вашої поїздки: {context.user_data["ride_type"]}\n\n{text}')

    if ride_type is ONE_TIME:
        return GET_DEPARTURE_TIME
    else:
        return GET_START_POINT


def get_departure_time(update, context):
    time_of_departure = update.message.text

    # adding vars to user_data
    context.user_data['time_of_departure'] = time_of_departure

    update.message.reply_text(f'Час вашого відправлення:{context.user_data["time_of_departure"]}\n\n'
                              f'Будь ласка, тепер введіть дату поїздки у форматі DD.MM.YYYY')
    return GET_DEPARTURE_DATE


def get_departure_date(update, context):
    date_of_departure = update.message.text

    # adding vars to user_data
    context.user_data['date_of_departure'] = date_of_departure

    update.message.reply_text(f'Дата вашого відправлення: {context.user_data["date_of_departure"]}.\n\n'
                              f'Тепер локацыю місця вашого відправлення:')
    return GET_START_POINT


def get_ride_type_or_start_point(update, context):
    if update.callback_query:
        query = update.callback_query
        ride_type = query.data
        # adding vars to user_data
        if ride_type is ONE_TIME:
            context.user_data['ride_type'] = 'ONE_TIME'
        else:
            context.user_data['ride_type'] = 'REGULAR'
        text = f'Тип вашої поїздки: {context.user_data["ride_type"]}'
        context.bot.send_message(chat_id=update.effective_message.chat_id, text=text)
    else:
        location = update.message.location
        latitude, longitude = location.latitude, location.longitude

        # adding vars to user_data
        context.user_data['start_latitude'] = latitude
        context.user_data['start_longitude'] = longitude

    context.bot.send_message(chat_id=update.effective_message.chat_id, text='А тепер вкажіть, куди ви прямуєте:')
    return GET_FINISH_POINT


def get_finish_point_and_send_requests(update, context):
    location = update.message.location
    latitude, longitude = location.latitude, location.longitude

    # adding vars to user_data
    context.user_data['finish_latitude'] = latitude
    context.user_data['finish_longitude'] = longitude

    if context.user_data['ride_type'] is 'ONE_TIME':
        text = f'Деталі поїздки, що будуть відправлені на сервер:\n'
        f'Тип поїдки: {context.user_data["ride_type"]}.'
        f'Час відправлення: {context.user_data["time_of_departure"]}.\n'
        f'Дата відправлення: {context.user_data["date_of_departure"]}.\n'
        f'Координати старту: {context.user_data["start_latitude"]}, {context.user_data["start_longitude"]}.\n'
        f'Координати фінішу: {context.user_data["finish_latitude"]}, {context.user_data["finish_longitude"]}\n'
    elif context.user_data['ride_type'] is 'REGULAR':
        text = f'Деталі поїздки, що будуть відправлені на сервер:\n'
        f'Тип поїдки: {context.user_data["ride_type"]}.'
        f'Координати старту: {context.user_data["start_latitude"]}, {context.user_data["start_longitude"]}.\n'
        f'Координати фінішу: {context.user_data["finish_latitude"]}, {context.user_data["finish_longitude"]}\n'

    # отправляем собраные данные -- POST
    # вызываем метод для получения -- GET
    return get_db_response(update, context)


def get_db_response(update, context):

    dummy_data = {'result_list': {
        1: {
            'user_first_name': 'Denis',
            'user_last_name': 'Kuznetsov',
            'user_phone_number': '+380997683348',
            'user_status': 'medic',
            'user_chat_id': '400427515',
            'time_of_departure': '08.00',
            'date_of_departure': '20.20.2020',
            'finish_point': {
                'latitude': '47.8154243',
                'longitude': '35.1920189'
            }
        },
        2: {
            'user_first_name': 'Some',
            'user_last_name': 'User',
            'user_phone_number': '+380997683348',
            'user_status': 'medic',
            'user_chat_id': '400427515',
            'time_of_departure': '21.00',
            'date_of_departure': '20.20.3333',
            'finish_point': {
                'latitude': '47.8516381',
                'longitude': '35.1303422'
            }
        }
    }}

    # отправляем запрос на наличие совпадений -- GET
    response = dummy_data

    # после отправки запроса перезаписываем содержимое user_data, чтобы передать их в get_details
    context.user_data.clear()
    context.user_data['response'] = response

    if len(context.user_data['response']['result_list']):
        if context.user_data['response']['result_list'][1]['user_status'] is 'medic':
            keyboard = [[InlineKeyboardButton("Деталі", callback_data=str(GET_DETAILS))]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text('Ми знайшли медиків поряд з місцем вашого відправлення!',
                                      reply_markup=reply_markup)
            return GET_RESULT_LIST
        else:
            update.message.reply_text("Поряд з місцем вашого відправлення знайшлися водії!\n"
                                      "Ми відправили їм ваши контакти, та інформацію про ваш маршрут.\n"
                                      "Можливо скоро з вами зв'яжуться!")
            return ConversationHandler.END
    else:
        update.message.reply_text('Наразі у систумі немає ваших попутників. Ми повідомимо, коли такі знайдуться.')
        return ConversationHandler.END










