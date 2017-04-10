import logging
from functools import wraps
from telegram.ext import CommandHandler, Updater
import config
from api_client import ApiClient
from formatter import Formatter

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=config.LOGLEVEL)

updater = Updater(token=config.BOT_TOKEN)
dispatcher = updater.dispatcher
api_client = ApiClient()
formatter = Formatter()


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

    result = api_client.make_request('GET', '/notes', headers={
        'token': config.USER_TOKENS.get(update.message.chat.username)
    })

    if result.get('success'):
        return bot.sendMessage(
            chat_id=update.message.chat_id,
            text=formatter.format_notes(result.get('data')),
            parse_mode='Markdown'
        )

    if isinstance(result.get('data'), dict):
        message = result.get('data').get('msg')
    else:
        message = result.get('data')

    bot.sendMessage(chat_id=update.message.chat_id, text=message)


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
