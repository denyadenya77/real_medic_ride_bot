from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Location
from telegram.ext import ConversationHandler
from vars_module import *
from route_requests import create_route_request, get_similar_routes_request


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

    update.effective_message.reply_text(f'Тип вашої поїздки: {context.user_data["ride_type"]}\n\n{text}')

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
    context.user_data['telegram_id'] = update.effective_message.chat_id

    response = None
    if context.user_data['ride_type'] == 'ONE_TIME':
        response = create_route_request(telegram_id=context.user_data['telegram_id'],
                                        time_of_departure=context.user_data['time_of_departure'],
                                        date_of_departure=context.user_data['date_of_departure'],
                                        start_latitude=context.user_data['start_latitude'],
                                        start_longitude=context.user_data['start_longitude'],
                                        finish_latitude=context.user_data["finish_latitude"],
                                        finish_longitude=context.user_data["finish_longitude"])
    elif context.user_data['ride_type'] == 'REGULAR':
        response = create_route_request(telegram_id=context.user_data['telegram_id'],
                                        start_latitude=context.user_data['start_latitude'],
                                        start_longitude=context.user_data['start_longitude'],
                                        finish_latitude=context.user_data["finish_latitude"],
                                        finish_longitude=context.user_data["finish_longitude"])

    if response.status_code == 201:
        update.effective_message.reply_text('Маршрут успешно добален в базу данных.')
    else:
        update.effective_message.reply_text('Произошла ошибка. Попробуйте внести маршрут в базу позже.')

    return get_db_response(update, context)


def get_db_response(update, context):

    # отправляем запрос на наличие совпадений -- GET
    if context.user_data['ride_type'] == 'ONE_TIME':
        response = get_similar_routes_request(telegram_id=context.user_data['telegram_id'],
                                              time_of_departure=context.user_data['time_of_departure'],
                                              date_of_departure=context.user_data['date_of_departure'],
                                              start_latitude=context.user_data['start_latitude'],
                                              start_longitude=context.user_data['start_longitude'],
                                              finish_latitude=context.user_data["finish_latitude"],
                                              finish_longitude=context.user_data["finish_longitude"])
    else:
        response = get_similar_routes_request(telegram_id=context.user_data['telegram_id'],
                                              start_latitude=context.user_data['start_latitude'],
                                              start_longitude=context.user_data['start_longitude'],
                                              finish_latitude=context.user_data["finish_latitude"],
                                              finish_longitude=context.user_data["finish_longitude"])


    # после отправки запроса перезаписываем содержимое user_data, чтобы передать их в get_details
    context.user_data.clear()
    context.user_data['response'] = response

    if len(context.user_data['response']):
        if context.user_data['response'][0]['user']['type'] == 'medic':
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










