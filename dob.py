# -*- coding: utf-8 -*-

from time import sleep
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
import logging

from f_gpio import *
from secretConf import *

## inizio impostazioni
allowedUsers=getAllowedUsers()
token=getToken()
## fine impostazioni

# variabili globali
stanza=""

locationPickerKeyboard = [
    [InlineKeyboardButton("Sala", callback_data="s"), InlineKeyboardButton("Cucina", callback_data="c")],
    [InlineKeyboardButton("Camera Fabio", callback_data="cf"), InlineKeyboardButton("Camera Sonia", callback_data="cs")],
    [InlineKeyboardButton("Tutto", callback_data='t')]
    ]

upDownKeyboard = [
    [InlineKeyboardButton("Sù", callback_data="u")],
    [InlineKeyboardButton("A metà", callback_data="m")],
    [InlineKeyboardButton("Giù", callback_data="d")]
    ]

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def convertName(oneLetterName):
    if oneLetterName=='s':
        return "sala"
    elif oneLetterName=='c':
        return "cucina"
    elif oneLetterName=='cf':
        return "camera di Fabio"
    elif oneLetterName=='cs':
        return "camera di Sonia"
    elif oneLetterName=='t':
        return "tutto"

def convertAction(ac):
    if ac=="u":
        return "salendo."
    elif ac=="m":
        return "andando a metà."
    elif ac=="d":
        return "scendendo."


def start(bot, update):
    reply_markup = InlineKeyboardMarkup(locationPickerKeyboard)

    user=update.effective_user.username

    if user not in allowedUsers:
        # se l'utente non è tra i presenti
        update.message.reply_text("This bot is no longer mainteined.")
        return

    update.message.reply_text("Ciao! Scegli quali tapparelle:", reply_markup=reply_markup)

def replyInline(bot, update):

    global stanza

    # query di ritorno
    query=update.callback_query
    # stringa di ritorno
    q=query.data

    if q=="u" or q=="d" or q=="m":
        # se ho trovato un up o un down chiamo le funzioni esterne
        bot.edit_message_text(text="La tapparella sta "+convertAction(q), chat_id=query.message.chat_id, message_id=query.message.message_id)
        movimento(stanza, q)
    else:
        # ho il valore di una stanza
        stanza=q
        kbrMarkup = InlineKeyboardMarkup(upDownKeyboard)
        bot.edit_message_text(text="Tapparelle "+convertName(query.data), chat_id=query.message.chat_id, message_id=query.message.message_id, reply_markup=kbrMarkup)



# Create the Updater and pass it your bot's token.
updater = Updater(token)

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CallbackQueryHandler(replyInline))

updater.start_polling()
updater.idle()
