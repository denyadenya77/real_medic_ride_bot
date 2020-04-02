from telegram import Location, Contact
from telegram.ext import ConversationHandler


def get_several_details_messages(update, context):
    result_list = context.user_data['response']['result_list']
    update.callback_query.edit_message_text('Ми знайшли медиків поряд з місцем вашого відправлення!')

    context.chat_data['info'] = {'count_of_active_messages': 0}

    for key, value in result_list.items():
        context.chat_data['info']['count_of_active_messages'] += 1

        location = Location(latitude=value['finish_point']['latitude'],
                            longitude=value['finish_point']['longitude'])

        contact = Contact(phone_number=value['user_phone_number'],
                          first_name=value['user_first_name'],
                          last_name=value['user_last_name'])

        context.bot.send_message(update.effective_message.chat_id,
                                 text=f'Час відправлення: {value["time_of_departure"]}.\n'
                                      f'Дата відправлення: {value["date_of_departure"]}.\n'
                                      f'Місце призначення:')
        context.bot.send_location(chat_id=update.effective_message.chat_id, location=location)
        context.bot.send_contact(update.effective_message.chat_id, contact=contact)

    result_list = context.user_data.clear()

    return ConversationHandler.END
