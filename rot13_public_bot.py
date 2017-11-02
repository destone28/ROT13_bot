#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages with the ROT13 translation of your
# message
# This program is dedicated to the public domain under the CC0 license.
"""
This Bot uses the Updater class to handle the bot.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, with added the ROT13 translator function.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import string

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.

def start(bot, update):
	update.message.reply_text('''Hello, I'm a ROT13 translator!
Send me a message, and I'll translate it for you in ROT13, one of the first and 
easier crypto algorithms created ever: with this, secret messages was exchanged 
by famous people like Giulio Cesare, Augusto e Bernardo Provenzano.
For more infos:
	https://en.wikipedia.org/wiki/Caesar_cipher
    and
    https://en.wikipedia.org/wiki/ROT13 ''')

def help(bot, update):
    start(bot, update)

def echo(bot, update):
    try:
        update.message.reply_text(rot13(str(update.message.text)))
    except UnicodeEncodeError:
        update.message.reply_text('ROT13 is for alphabetical character, I can''t
 translate. Inserisci le stesse lettere senza accenti! Ah, e non so leggere le emoticon! :-)')

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def rot13(testo):                               #funzione traduzione in rot13
    alfabeto_min = string.lowercase
    alfabeto_mai = string.uppercase
    alfabeto = alfabeto_min + alfabeto_mai
    alfabeto_rot13_min = alfabeto_min[13:] + alfabeto_min[:13]
    alfabeto_rot13_mai = alfabeto_mai[13:] + alfabeto_mai[:13]
    alfabeto_rot13 = alfabeto_rot13_min + alfabeto_rot13_mai
    return string.translate(testo, string.maketrans(alfabeto, alfabeto_rot13))

def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("334782389:AAHvSV8jSsJz1pd1xeDMJlfMmodwr1tO3a8")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
