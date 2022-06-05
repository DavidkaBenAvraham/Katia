#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=W0613, C0116
# type: ignore[union-attr]
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

import bot.messenger_db as messanger
import bot.bot_keyboard as kb
import DB as db
import time

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')
    kb.start_kb(update, context)

adv_list = []
start_send = True
def start_sender(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    global adv_list
    global start_send
    if len(context.args)>0: 
        pause = float(context.args[0])
        adv_list = messanger.get_adv_from_db()
        for adv in adv_list:
            update.message.reply_text(f'start_send {start_send}')
            update.message.reply_text(f'{adv}')
            time.sleep(pause)
            if start_send == False: return

    else: update.message.reply_text(' /start_sender pause in <seconds> ')


def adv(adv_list:[]) -> str:pass

def stop_sender(update: Update, context: CallbackContext) -> None:
    #chat_id = update.message.chat_id
    #job_removed = remove_job_if_exists(str(chat_id), context)
    #update.message.reply_text(f'chat {chat_id} stopped = {job_removed}')
    global start_send
    start_send = False

    chat_id = update.message.chat_id
    update.message.reply_text(f'chat {chat_id} stopped ')

    pass

################################################### JOB

def remove_job_if_exists(name, context):
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True

def get_jobs_list(update: Update, context: CallbackContext) -> None:
    """ возвращает список запущенных задач ."""
    chat_id = update.message.chat_id
    current_jobs = context.job_queue.get_jobs_by_name(str(chat_id))
    if not current_jobs:
        update.message.reply_text(f'Нет запущенных задач')
    for job in current_jobs:
        update.message.reply_text(f'задача {job}')
    return True

def get_chat_id(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    update.message.reply_text(f'chat id {chat_id}')

def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""

    help_msg = str(f'''
    Commands:
    /start_sender [10] - 
    /stop_sender - 
    /get_kb - Get keyboard
    /jobs - Get list of current jobs
    /chat - Get chat ID
    ''')

    update.message.reply_text(help_msg)


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def sendme_message(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'''Write message <message> ''')

#def add_adv():
#    db.execute(guery)
#    return db.execute(guery)

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    token = '1346001134:AAFBJwqF9kFrOYgVLxJshtN6cQzwwB8mLBM'
    updater = Updater(token, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("sendme_message", sendme_message))
    dispatcher.add_handler(CommandHandler("start_sender", start_sender))
    dispatcher.add_handler(CommandHandler("stop_sender", stop_sender))
    dispatcher.add_handler(CommandHandler("get_kb", kb.get_kb))
    dispatcher.add_handler(CommandHandler("jobs", get_jobs_list))
    dispatcher.add_handler(CommandHandler("chat", get_chat_id))
    
    # on noncommand i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    dispatcher.add_handler(CallbackQueryHandler(kb.button))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
