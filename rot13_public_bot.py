#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot that reply to Telegram messages with a ROT13 translation of what is sent to it
"""
This Bot uses the Updater class to handle the bot.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
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
    update.message.reply_text('''Hello, I'm a ROT13 translator! Send me something and I'll translate it for you in Rot13, one of the first and easier crypto algorithms: based on this model people like Giulio Cesare, Augusto and Bernardo Provenzano exchanged their secret messages.
    More infos about:
    https://en.wikipedia.org/wiki/Caesar_cipher    and
    https://en.wikipedia.org/wiki/ROT13 ''')

def help(bot, update):
    start(bot, update)

def echo(bot, update):
    try:
        update.message.reply_text(rot13(str(update.message.text)))
    except UnicodeEncodeError:
        update.message.reply_text("I can handle only alphabetical characters, so I can't translate accents. Insert the same letters without accents! And... I can't read emoticons! :-)")

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def rot13(text):                     #rot13 translator function
    alphabet_min = string.lowercase
    alphabet_mai = string.uppercase
    alphabet = alphabet_min + alphabet_mai
    alphabet_rot13_min = alphabet_min[13:] + alphabet_min[:13]
    alphabet_rot13_mai = alphabet_mai[13:] + alphabet_mai[:13]
    alphabet_rot13 = alphabet_rot13_min + alphabet_rot13_mai
    return string.translate(text, string.maketrans(alphabet, alphabet_rot13))

def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("YOUR_TOKEN_HERE")

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
