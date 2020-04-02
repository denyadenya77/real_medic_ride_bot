from telegram.ext import ConversationHandler, Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import os
from dotenv import load_dotenv
from adding_ride_funcs_2 import add_ride, get_ride_status_and_user_id, get_departure_time, get_departure_date, \
    get_ride_type_or_start_point, get_finish_point_and_send_requests
from other_funcs import start, cancel
from register_funcs import register, get_user_status
from view_details_funcs import get_several_details_messages
from vars_module import *

load_dotenv()


def main():
    updater = Updater(os.getenv("BOT_TOKEN"), use_context=True)
    dp = updater.dispatcher

    start_handler = CommandHandler('start', start)

    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('register', register, pass_user_data=True),
                      CommandHandler('add_ride', add_ride, pass_user_data=True)],
        states={
            GET_USER_STATUS: [CallbackQueryHandler(get_user_status, pattern=f'^{str(DRIVER)}$|^{str(DOCTOR)}$')],
            GET_RIDE_STATUS: [CallbackQueryHandler(get_ride_status_and_user_id, pattern=f'^{str(ONE_TIME)}$|^{str(REGULAR)}$')],
            GET_DEPARTURE_TIME: [MessageHandler(Filters.text, get_departure_time, pass_user_data=True)],
            GET_DEPARTURE_DATE: [MessageHandler(Filters.text, get_departure_date, pass_user_data=True)],
            GET_START_POINT: [MessageHandler(Filters.text, get_ride_type_or_start_point, pass_user_data=True)],
            GET_FINISH_POINT: [MessageHandler(Filters.text, get_finish_point_and_send_requests, pass_user_data=True)],
            # ниже - conversation для получения инфы о совпадении
            GET_RESULT_LIST: [CallbackQueryHandler(get_several_details_messages,
                                                   pattern=f'^{str(GET_DETAILS)}$',
                                                   pass_user_data=True)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dp.add_handler(start_handler)
    dp.add_handler(conversation_handler)

    # Getting mode, so we could define run function for local and Heroku setup
    mode = os.getenv("MODE")
    token = os.getenv("BOT_TOKEN")
    if mode == "dev":
        updater.start_polling()
    elif mode == "prod":
        port = int(os.environ.get("PORT", "8443"))
        heroku_app_name = os.environ.get("HEROKU_APP_NAME")
        updater.start_webhook(listen="0.0.0.0",
                              port=port,
                              url_path=token)
        updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(heroku_app_name, token))


if __name__ == '__main__':
    main()
