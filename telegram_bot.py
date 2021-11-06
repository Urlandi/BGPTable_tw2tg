# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, Filters, MessageFilter
from telegram import TelegramError

from config_telegram_auth import TOKEN
from telegram_bot_handlers import start_cmd, stop_cmd, settings_cmd, help_cmd, echo_cmd, last_status_cmd
from telegram_bot_handlers import telegram_error
from resources_messages import keyboard_buttons_name

import logging


class FilterLastStatus(MessageFilter):
    def filter(self, message):
        return keyboard_buttons_name["last_status_name"] == message.text


class FilterSettings(MessageFilter):
    def filter(self, message):
        return keyboard_buttons_name["settings_name"] == message.text


class FilterHelp(MessageFilter):
    def filter(self, message):
        return keyboard_buttons_name["help_name"] == message.text


def telegram_connect():

    try:
        updater = Updater(token=TOKEN)
        dispatcher = updater.dispatcher

        dispatcher.add_handler(CommandHandler("start", start_cmd))
        dispatcher.add_handler(CommandHandler("stop", stop_cmd))

        dispatcher.add_handler(CommandHandler("help", help_cmd))
        dispatcher.add_handler(MessageHandler(FilterHelp(), help_cmd))

        dispatcher.add_handler(CommandHandler("settings", settings_cmd))
        dispatcher.add_handler(MessageHandler(FilterSettings(), settings_cmd))
        dispatcher.add_handler(CallbackQueryHandler(settings_cmd))

        dispatcher.add_handler(CommandHandler("status", last_status_cmd))
        dispatcher.add_handler(MessageHandler(FilterLastStatus(), last_status_cmd))

        dispatcher.add_handler(MessageHandler(Filters.all, echo_cmd))

        dispatcher.add_error_handler(telegram_error)

        updater.start_polling(drop_pending_updates=True)  # God save the GIL

    except TelegramError as e:
        logging.fatal("Can't connect to telegram - {}".format(e))
        return None

    return updater
