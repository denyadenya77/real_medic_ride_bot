from telegram.ext import ConversationHandler


# other commands

def start(update, context):
    update.message.reply_text(f'Вітаємо! Тут буде інструкція з користування.\nЧат айди: {update.message.chat.id}')


def cancel(update, context):
    return ConversationHandler.END
