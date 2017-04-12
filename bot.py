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


def log_command(fn):
    """
    Logs user's command
    :param callable fn: 
    :return callable: 
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        log_user_message(args[1])
        return fn(*args, **kwargs)
    return wrapper


@check_username
@log_command
def start(bot, update):
    """
    Start conversation handler
    :param Bot bot: 
    :param Update update: 
    :return: 
    """
    bot.sendMessage(chat_id=update.message.chat_id, text="Hello")


@check_username
@log_command
def show_notes(bot, update):
    """
    Show notes handler
    :param Bot bot: 
    :param Update update: 
    :return: 
    """
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


@check_username
@log_command
def create_note(bot, update):
    """
    Creates note
    :param Bot bot: 
    :param Update update: 
    :return: 
    """
    command_body = get_command_body(update)

    if not command_body:
        return bot.sendMessage(
            chat_id=update.message.chat_id,
            text='Error creating note: empty command body.'
        )

    result = api_client.make_request(
        'POST',
        '/notes',
        json={'header': command_body.get('body')},
        headers={'token': config.USER_TOKENS.get(update.message.chat.username)}
    )

    if result.get('success'):
        return bot.sendMessage(
            chat_id=update.message.chat_id,
            text=formatter.format_created_note(result.get('data')),
            parse_mode='Markdown'
        )

    bot.sendMessage(
        chat_id=update.message.chat_id,
        text=result.get('data')
    )


@check_username
@log_command
def edit_note_body(bot, update):
    """
    Edits message body
    :param Bot bot: 
    :param Update update: 
    :return: 
    """
    command_body = get_command_body(update, with_id=True)

    if not command_body:
        return bot.sendMessage(
            chat_id=update.message.chat_id,
            text='Error editing note body: empty command body.'
        )

    result = api_client.make_request(
        'PUT',
        '/notes/{}'.format(command_body.get('id')),
        json={'body': command_body.get('body')},
        headers={'token': config.USER_TOKENS.get(update.message.chat.username)}
    )

    if result.get('success'):
        return bot.sendMessage(
            chat_id=update.message.chat_id,
            text=formatter.format_edited_note(result.get('data')),
            parse_mode='Markdown'
        )

    bot.sendMessage(
        chat_id=update.message.chat_id,
        text=result.get('data')
    )

@check_username
@log_command
def edit_note_header(bot, update):
    """
    Edits note header
    :param Bot bot: 
    :param Update update: 
    :return: 
    """
    command_body = get_command_body(update, with_id=True)

    if not command_body:
        return bot.sendMessage(
            chat_id=update.message.chat_id,
            text='Error editing note header: empty command body.'
        )

    result = api_client.make_request(
        'PUT',
        '/notes/{}'.format(command_body.get('id')),
        json={'header': command_body.get('body')},
        headers={'token': config.USER_TOKENS.get(update.message.chat.username)}
    )

    if result.get('success'):
        return bot.sendMessage(
            chat_id=update.message.chat_id,
            text=formatter.format_edited_note(result.get('data')),
            parse_mode='Markdown'
        )

    bot.sendMessage(
        chat_id=update.message.chat_id,
        text=result.get('data')
    )


@check_username
@log_command
def delete_note(bot, update):
    """
    Removes note
    :param Bot bot: 
    :param Update update: 
    :return: 
    """
    note_id = get_note_id(update)

    if not note_id:
        return bot.sendMessage(
            chat_id=update.message.chat_id,
            text='Error removing a note: empty note id.'
        )

    result = api_client.make_request(
        'DELETE',
        '/notes/{}'.format(note_id),
        headers={'token': config.USER_TOKENS.get(update.message.chat.username)}
    )

    if result.get('success'):
        return bot.sendMessage(
            chat_id=update.message.chat_id,
            text='Note has been deleted.',
        )

    bot.sendMessage(
        chat_id=update.message.chat_id,
        text=result.get('data')
    )


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


def get_command_body(update, with_id=False):
    """
    Returns command body
    :param Update update:
    :param bool with_id:
    :return:
    """
    command_list = update.message.text.split(' ')

    if with_id and len(command_list) > 2:
        return {
            'id': command_list[1],
            'body': ' '.join(command_list[2:])
        }

    if not with_id and len(command_list) > 1:
        return {
            'body': ' '.join(command_list[1:])
        }

    return None


def get_note_id(update):
    """
    Returns note_id
    :param Update update: 
    :return: 
    """
    command_list = update.message.text.split(' ')
    if len(command_list) == 2:
        return command_list[1].strip()

    return None

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('sn', show_notes))
dispatcher.add_handler(CommandHandler('cn', create_note))
dispatcher.add_handler(CommandHandler('enb', edit_note_body))
dispatcher.add_handler(CommandHandler('enh', edit_note_header))
dispatcher.add_handler(CommandHandler('dn', delete_note))

updater.start_polling()
