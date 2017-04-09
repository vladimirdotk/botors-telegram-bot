import logging
from functools import wraps
from telegram.ext import CommandHandler, Updater
import requests
import config

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

updater = Updater(token=config.BOT_TOKEN)
dispatcher = updater.dispatcher


def check_username(fn):
    """
    Checks username decorator
    :param callable fn: 
    :return callable: 
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if args[1].message.chat.username in config.USER_TOKENS:
            return fn(*args, **kwargs)

    return wrapper


@check_username
def start(bot, update):
    """
    Start conversation handler
    :param Bot bot: 
    :param Update update: 
    :return: 
    """
    log_user_message(update)
    bot.sendMessage(chat_id=update.message.chat_id, text="Hello")


@check_username
def show_notes(bot, update):
    """
    Show notes handler
    :param Bot bot: 
    :param Update update: 
    :return: 
    """
    log_user_message(update)
    data = requests.get('http://localhost:8003/notes', headers={
        'token': config.USER_TOKENS.get(update.message.chat.username)
    })
    bot.sendMessage(chat_id=update.message.chat_id, text=data.text)


def log_user_message(update):
    """
    Logs received message
    :param Update update: 
    :return: 
    """
    logging.info(
        'Received {} from {} {} (nick {})'.format(
            update.message.text,
            update.message.chat.first_name,
            update.message.chat.last_name,
            update.message.chat.username
        )
    )

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('sn', show_notes))

updater.start_polling()
