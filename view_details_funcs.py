from telegram import Location, Contact
from telegram.ext import ConversationHandler


def get_several_details_messages(update, context):
    result_list = context.user_data['response']
    update.callback_query.edit_message_text('Ми знайшли медиків поряд з місцем вашого відправлення!')

    for route in result_list:
        location = Location(latitude=route['finish_point']['latitude'],
                            longitude=route['finish_point']['longitude'])
        contact = Contact(phone_number=route['user']['phone_number'],
                          first_name=route['user']['first_name'],
                          last_name=route['user']['last_name'])

        if route.get('date_and_time'):

            date = route['date_and_time'][:10]
            time = route['date_and_time'][11:16]

            text = f'Время и дата отправления: {date}, {time}.\n' \
                   f'Місце призначення:'
        else:
            text = 'Регулярная поездка.\n' \
                   'Место назначения:'

        context.bot.send_message(update.effective_message.chat_id, text=text)
        context.bot.send_location(chat_id=update.effective_message.chat_id, location=location)
        context.bot.send_contact(update.effective_message.chat_id, contact=contact)

    context.bot.send_message(update.effective_message.chat_id, "Перегляньте місця призначення. Якщо вам по дорозі, "
                                                               "будь ласка, зв'яжіться з медиком, аби домовитися про "
                                                               "поїздку!")

    context.user_data.clear()

    return ConversationHandler.END
